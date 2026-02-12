from onebeam_agent_runtime.providers.base_provider import LLMProvider

class GeminiProvider(LLMProvider):

    def generate_structured_output(self, system_prompt, user_prompt, tools, output_schema):

        return {
            "tool_name": "create_workflow",
            "arguments": {
                "name": "Overdue Task Handler",
                "trigger": "task.overdue",
                "steps": [
                    {
                        "type": "update",
                        "entity": "Task",
                        "update": {"status": "urgent"}
                    }
                ]
            }
        }
