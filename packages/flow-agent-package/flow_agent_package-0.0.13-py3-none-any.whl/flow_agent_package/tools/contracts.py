from dataclasses import dataclass, is_dataclass
from enum import Enum


@dataclass
class AgentSkillConfiguration:
    name: str
    description: str
    flow_name: str


class ArbitrationMethod(Enum):
  LANGCHAIN = "Langchain"
  OPENAI_FUNCTIONS = "OpenAI Functions"
  SEMANTIC_KERNEL = "Semantic Kernel"