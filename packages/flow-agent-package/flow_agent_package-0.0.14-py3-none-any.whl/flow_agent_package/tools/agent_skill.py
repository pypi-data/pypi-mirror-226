from promptflow.azure import PFClient

from semantic_kernel.skill_definition import sk_function

from flow_agent_package.tools.contracts import AgentSkillConfiguration
from flow_agent_package.tools.flow_manager import FlowManager

class AgentSkill():

  def __init__(self, config: AgentSkillConfiguration, pf: PFClient, subscription_id, resource_group, workspace_name):
      self.name = config.name
      self.tool_description = config.description
      self.flow_manager = FlowManager(pf, config.flow_name, subscription_id, resource_group, workspace_name)
      
      self.function_description = self.init_description(self.flow_manager.flow_json, config)
      self.input_config = self.init_inputs(self.flow_manager.flow_json)
      self.output = self.init_output(self.flow_manager.flow_json)

  def init_inputs(self, flow_json):
    base_inputs = flow_json["flow"]["inputs"]
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
    return input_config
  
  def init_output(self, flow_json):
    outputs = flow_json["flow"]["outputs"]
    if len(outputs.keys()) != 1:
      raise Exception("Skills used in agent must have only one output!")
    return list(outputs.keys())[0]
  
  def init_description(self, flow_json, config):
    config_desc = config.description
    # In case of default desc, use tool description
    if flow_json.get("description") == "Template Standard Flow":
      return config_desc
    return flow_json.get("description", config_desc)

  def to_function_definition(self):
    return {
      "name": self.flow_manager.flow_json["flowName"].replace(" ", "_"),
      "description": self.function_description,
      "parameters":{
        "type": "object",
        "properties": self.input_config
      }
    }

  def to_langchain_function(self):
      
      def run_str(query):
          result = self.execute(query)
          return result
      
      return run_str

  def to_sk_function(self):
    @sk_function(
        description=self.function_description,
        name=self.name
    )
    def sk_execute_func(query: str) -> str:
      result = self.execute(query)
      return result
    return sk_execute_func

  def execute(self, inputs) -> dict:
    try:
      return self.flow_manager.execute_flow(inputs)
    except Exception as e:
      print(f"Exception encountered: {str(e)}")
      return f"Exception encountered when calling tool {self.name}: {str(e)}"
