# onebeam_agent_runtime/schemas/workflow_schema.py

WORKFLOW_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "trigger": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "entity": {"type": "string"},
                    "update": {"type": "object"}
                },
                "required": ["type", "entity", "update"]
            }
        }
    },
    "required": ["name", "trigger", "steps"]
}
