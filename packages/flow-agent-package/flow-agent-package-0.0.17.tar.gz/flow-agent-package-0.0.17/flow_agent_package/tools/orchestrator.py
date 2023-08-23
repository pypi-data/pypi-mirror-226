import json

from semantic_kernel import Kernel
from semantic_kernel.skill_definition import (
    sk_function,
)
from semantic_kernel.orchestration.sk_context import SKContext


class OrchestratorPlugin:
  def __init__(self, kernel: Kernel):
      self._kernel = kernel

  @sk_function(
      description="Routes the request to the appropriate function",
      name="route_request",
  )
  async def RouteRequest(self, context: SKContext) -> str:
      # Save the original user request
      print("Routing Request")
      request = context["input"]
      try:
        history = context["history"]
      except:
        history = []
      native_funcs = self._kernel.skills.get_functions_view().native_functions["FlowPlugin"]
      func_options = [function.name for function in native_funcs]
      print(f"Functions returned {func_options}")
      # Add the list of available functions to the context
      context["options"] = " ,".join(func_options)
        
      # Retrieve the intent from the user request
      GetIntent = self._kernel.skills.get_function("OrchestratorPlugin", "GetIntent")
      FormatResponse = self._kernel.skills.get_function(
          "OrchestratorPlugin", "FormatResponse"
      )
      
      await GetIntent.invoke_async(context=context)
      intent = context["input"].strip()
      
      print(f"context: {intent}")
      
      picked_function = self._kernel.skills.get_function("FlowPlugin", intent)

      # Create a new context object with the original request
      pipelineContext = self._kernel.create_new_context()
      pipelineContext["original_request"] = request
      pipelineContext["input"] = request
      pipelineContext["tool_name"] = intent
      

      if len(history) != 0:
        print("Using History")
        
        pipelineContext["history"] = history
        ExtractInputs = self._kernel.skills.get_function(
            "OrchestratorPlugin", "ExtractInputs"
        )
        ExtractQueryFromJson = self._kernel.skills.get_function(
          "OrchestratorPlugin", "ExtractQueryFromJson"
        )
        # Run the functions in a pipeline
        output = await self._kernel.run_async(
            ExtractInputs,
            ExtractQueryFromJson,
            picked_function,
            input_context=pipelineContext,
        )
      else:
        # Run the functions in a pipeline
        output = await self._kernel.run_async(
            picked_function,
            input_context=pipelineContext,
        )
        print(f"Final output: {output}")
      return output["input"]
  
  @sk_function(
    description="Extracts query from JSON",
    name="ExtractQueryFromJson",
  )
  def ExtractQueryFromJson(self, context: SKContext):
      query_json = json.loads(context["input"])

      context["input"] = query_json["query"]
      print(f"Extracted Input: {query_json['query']}")

      return context
