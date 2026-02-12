from jsonschema import validate, ValidationError

from onebeam_agent_runtime.core.model_router import get_model_provider
from onebeam_agent_runtime.core.permission_guard import check_permission
from onebeam_agent_runtime.tools.tool_registry import TOOL_REGISTRY
from onebeam_agent_runtime.core.logger import log_action
from onebeam_agent_runtime.schemas.workflow_schema import WORKFLOW_SCHEMA


class AgentRuntime:

    def validate_output(self, result):
        try:
            validate(instance=result["arguments"], schema=WORKFLOW_SCHEMA)
        except ValidationError as e:
            raise Exception(f"Schema validation failed: {e.message}")

    def run(self, agent_config, user_input, mode="discussion"):

        provider = get_model_provider(agent_config["model"])

        result = provider.generate_structured_output(
            system_prompt=agent_config["instructions"],
            user_prompt=user_input,
            tools=[],
            output_schema=WORKFLOW_SCHEMA
        )

        # 🔒 ALWAYS validate before anything else
        self.validate_output(result)

        if mode == "discussion":
            print("=== DISCUSSION MODE ===")
            print(result)
            return result

        if mode == "execution":

            check_permission(agent_config, result["tool_name"])

            tool_function = TOOL_REGISTRY[result["tool_name"]]
            output = tool_function(result["arguments"])

            log_action("Tool executed: " + result["tool_name"])
            return output

