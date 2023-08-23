import requests
import uuid
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime

from azureml.core import Workspace
from azureml.core.authentication import TokenAuthentication

from azure.mgmt.storage import StorageManagementClient
from azure.storage.fileshare import ShareServiceClient
from azure.identity import DefaultAzureCredential

from flow_agent_package.tools.utils import get_token_for_audience, wait_for_completion, custom_active_instance

from promptflow.contracts.run_mode import RunMode
from promptflow.runtime.contracts.runtime import SubmitFlowRequest
from promptflow.core.thread_local_singleton import ThreadLocalSingleton
from promptflow.runtime import PromptFlowRuntime


class FlowManager:

    def __init__(self, client, flow_name, subscription_id, resource_group, workspace_name):
        self.client = client
        self.flow_name = flow_name
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name

        self.flow_dto = self.get_flow_dto_from_name()
        self.flow_json = self.get_flow_json_from_dto()
        self.init_inputs()
        self.init_output()
        if self.flow_dto.flow_definition_file_path:
            self.is_code_first = True
        else:
            self.is_code_first = False
    
    def get_flow_dto_from_name(self):
        # List all flows
        all_flows = self.client._flows._service_caller.list_flows(self.subscription_id, self.resource_group, self.workspace_name)

        for flow in all_flows:
            if flow.flow_name == self.flow_name:
                return flow
        
        raise Exception(f"Flow {self.flow_name} does not exist in workspace {self.workspace_name}")
    
    def get_flow_json_from_dto(self):
        workspace = Workspace(subscription_id=self.subscription_id, resource_group=self.resource_group, workspace_name=self.workspace_name, auth= TokenAuthentication(get_token_for_audience))
        endpoint = workspace.service_context._get_endpoint('api')
        url = f"{endpoint}/flow/api/subscriptions/{workspace.subscription_id}/resourcegroups/" + \
                f"{workspace.resource_group}/providers/Microsoft.MachineLearningServices/workspaces/" + \
                f"{workspace.name}/Flows/{self.flow_dto.flow_id}?experimentId={self.flow_dto.experiment_id}"
        
        token = get_token_for_audience(None)
        headers = {
            'Authorization': f'Bearer {token}',
            'content-type': 'application/json'
        }
        flow_json = requests.get(url, headers=headers).json()

        graph = flow_json["flow"]["flowGraph"]
        batch_inputs = flow_json["flowRunSettings"]["batch_inputs"]
            
        final_json = {
            "flowName": self.flow_dto.flow_name,
            "description": self.flow_dto.description,
            "flowId": self.flow_dto.flow_id,
            "flow": graph,
            "batch_inputs": batch_inputs,
        }

        return final_json

    def init_inputs(self):
        base_inputs = self.flow_json["flow"]["inputs"]
        input_config = {}
        for input_name, input_info in base_inputs.items():
            input_type = input_info.get("type")
            if input_type == None:
                raise Exception(f"Input {input_name} for tool {self.name} does not have a type specified!")
            # elif input_type == "object"
            #   raise Exception(f"Input {input_name} for tool {self.name} has incompatible type: {input_type}")
            
            input_description = input_info.get("description")
            # if input_description == None:
            #   raise Exception(f"Input {input_name} for tool {self.name} does not have a description!")
            temp = {"type": input_type}
            if input_description:
                temp["description"] = input_description
            input_config[input_name] = temp
        self.input_config = input_config
  
    def init_output(self):
        outputs = self.flow_json["flow"]["outputs"]
        if len(outputs.keys()) != 1:
            raise Exception("Skills used in agent must have only one output!")
        self.output = list(outputs.keys())[0]

    def execute_flow(self, inputs):
        if self.is_code_first:
            return self.execute_yaml_flow(inputs)
        else:
            return self.execute_json_flow(inputs)

    def execute_yaml_flow(self, inputs):
        with tempfile.TemporaryDirectory() as tmpdirname:
            print('created temporary directory', tmpdirname)
            self.download_all_flow_files(tmpdirname)
            flow_path = os.path.join(tmpdirname, "flow.dag.yaml")
            if isinstance(inputs, str):
                new_inputs = {}
                for key in self.input_config:
                    new_inputs[key] = inputs
                new_inputs = [new_inputs]
            elif isinstance(inputs, dict):
                new_inputs = [inputs]
            else:
                raise Exception(f"Incorrect input format: {type(inputs)}")
            input_path = os.path.join(tmpdirname, "data.jsonl")
            with open(input_path, 'w') as f:
                f.write('\n'.join(map(json.dumps, new_inputs)))
            base_run = self.client.run(flow=flow_path, data=input_path, runtime="agent-runtime-3")
            wait_for_completion(base_run, 5)
            return self.client.get_details(base_run)[f"outputs.{self.output}"][0]

    def execute_json_flow(self, inputs) -> str:
        # GET CONNECTIONS HERE
        flow_request = self.create_submit_flow_request(inputs, None, RunMode.Flow)
        
        ThreadLocalSingleton._activate_in_context = custom_active_instance

        runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
        start = datetime.now()
        old_setting = runtime.config.execution.execute_in_process
        runtime.config.execution.execute_in_process = False
        
        result = runtime.execute(flow_request)
        runtime.config.execution.execute_in_process = old_setting
        end = datetime.now()
        print(f"ORiginal result: {result}")
        result = result["flow_runs"][0]["output"][self.output][0]
        return result

    def set_connection_info(self):
        workspace = Workspace(subscription_id=self.subscription_id, resource_group=self.resource_group, workspace_name=self.workspace_name, auth= TokenAuthentication(get_token_for_audience))
        endpoint = workspace.service_context._get_endpoint('api')
        graph = self.flow_json["flow"]
        connections = []
        for node in graph["nodes"]:
            if node.get("connection"):
                connections.append(node.get("connection"))
            if node.get("inputs", {}).get("connection"):
                connections.append(node["inputs"]["connection"])
        connection_configs = {}
        token = get_token_for_audience(None)
        headers = {
            'Authorization': f'Bearer {token}',
            'content-type': 'application/json'
        }
        for connection_name in set(connections):
            url = f"{endpoint}/rp/workspaces/subscriptions/{workspace.subscription_id}/resourcegroups/" + \
            f"{workspace.resource_group}/providers/Microsoft.MachineLearningServices/workspaces/" + \
            f"{workspace.name}/connections/{connection_name}/listsecrets?api-version=2023-02-01-preview"

            
            connection_json = requests.post(url, headers=headers).json()
            config = {
                "type": "AzureOpenAIConnection",
                "value": {
                    "api_key": connection_json["properties"]["credentials"]["key"],
                    "api_base": connection_json["properties"]["target"],
                    "api_type": "azure",
                    "api_version": "2023-03-15-preview"
                }
            }
            connection_configs[connection_name] = config
        self.flow_json["connections"]= connection_configs
    
    def create_submit_flow_request(
        self,
        inputs,
        source_run_id=None,
        run_mode: RunMode = RunMode.Flow,
    ) -> dict:
        """Refine the request to raw request dict"""
        if self.flow_json.get("connections") == None:
            self.set_connection_info()

        request = self.flow_json
        flow_run_id = str(uuid.uuid4())
        if not source_run_id:
            source_run_id = str(uuid.uuid4())
        variant_runs = request.get("variants_runs", {})
        if variant_runs:
            request["variants_runs"] = {v: f"{vid}_{flow_run_id}" for v, vid in variant_runs.items()}
        if request.get("eval_flow_run_id"):
            request["eval_flow_run_id"] = f"{request['eval_flow_run_id']}_{flow_run_id}"
        if "id" not in request["flow"]:
            request["flow"]["id"] = str(uuid.uuid4())
        if isinstance(inputs, str):
            old_inputs = request["batch_inputs"]
            for key in old_inputs[0]:
                old_inputs[0][key] = inputs
            request["batch_inputs"] = old_inputs
        elif isinstance(inputs, dict):
            request["batch_inputs"] = [inputs]

        print(f"final inputs: {request['batch_inputs']}")
        request_json =  {
            "FlowId": request["flow"]["id"],
            "FlowRunId": flow_run_id,
            "SourceFlowRunId": source_run_id,
            "SubmissionData": json.dumps(request),
            "RunMode": run_mode,
            "BatchDataInput": request.get("batch_data_input", {}),
        }
        return SubmitFlowRequest.deserialize(request_json)
    
    def get_file_share_client(self):
        print("Getting file share client")
        ws = Workspace(subscription_id=self.subscription_id, resource_group=self.resource_group, workspace_name=self.workspace_name, auth= TokenAuthentication(get_token_for_audience))
        details = ws.get_details()
        print("Got workspace details")
        storage_account = details["storageAccount"]
        storage_account_name = storage_account.split("/")[-1]
        print(f"Workspace Storage Account Name: {storage_account_name}")
        storage_client = StorageManagementClient(DefaultAzureCredential(), self.subscription_id)
        storage_url = f"https://{storage_account_name}.file.core.windows.net"
        storage_key = storage_client.storage_accounts.list_keys(self.resource_group, storage_account_name).keys[0].value
        file_service_client = ShareServiceClient(
            account_url=storage_url,
            credential=storage_key,
            token_intent="file"
        )
        code_share_client = file_service_client.get_share_client("code-391ff5ac-6576-460f-ba4d-7e03433c68b6")
        return code_share_client
    
    def download_all_flow_files(self, working_directory, directory_client = None):
        if not directory_client:
            file_client = self.get_file_share_client()
            file_definition_path = self.flow_dto.flow_definition_file_path
            absolute_path = Path(file_definition_path).parent
            print(f"Path to Code: {absolute_path}")
            directory_client = file_client.get_directory_client(str(absolute_path))
        
        file_dir_list = directory_client.list_directories_and_files()
        for item in file_dir_list:
            if not (item.name.startswith("__")):
                if item.is_directory:
                    print(f"Downloading Directory: {item}")
                    sub_path = os.path.join(working_directory, item.name)
                    if not os.path.exists(sub_path):
                        os.makedirs(sub_path)
                    self.download_all_flow_files(sub_path, directory_client.get_subdirectory_client(item.name))
                    print("Downloaded Directory")
                else:
                    print(f"File: {item}")
                    file_client = directory_client.get_file_client(item.name)
                    file_path = os.path.join(working_directory, item.name)
                    with open(file_path, "wb") as data:
                        stream = file_client.download_file()
                        data.write(stream.readall())
                    print(f"File downloaded")