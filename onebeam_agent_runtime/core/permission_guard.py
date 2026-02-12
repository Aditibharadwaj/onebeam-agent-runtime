def check_permission(agent_config, tool_name):

    if tool_name not in agent_config["allowed_tools"]:
        raise Exception("Tool not allowed for this agent")
