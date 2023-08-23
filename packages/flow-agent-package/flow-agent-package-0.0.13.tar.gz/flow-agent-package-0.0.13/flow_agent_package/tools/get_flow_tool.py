from promptflow import tool
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
from flow_agent_package.tools.contracts import AgentSkillConfiguration


@tool
def get_flow_tool(name: str, description: str, flow_name: str):
  config = AgentSkillConfiguration(name, description, flow_name=flow_name)
  return config
