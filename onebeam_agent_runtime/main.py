import argparse

from onebeam_agent_runtime.core.agent_runtime import AgentRuntime
from onebeam_agent_runtime.agents.workflow_agent import WORKFLOW_AGENT


def main():
    parser = argparse.ArgumentParser(description="Run Onebeam Agent")

    parser.add_argument(
        "--model",
        type=str,
        help="Override model (gpt-5.2, claude-opus-4.6, gemini-3)"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="discussion",
        help="Mode: discussion or execution"
    )

    parser.add_argument(
        "--confirm",
        type=str,
        help="Confirmation required for execution (yes)"
    )

    args = parser.parse_args()

    agent_config = WORKFLOW_AGENT.copy()

    # Model override
    if args.model:
        print(f"Overriding model to: {args.model}")
        agent_config["model"] = args.model

    runtime = AgentRuntime()

    # Enforce confirmation for execution
    if args.mode == "execution":
        if args.confirm != "yes":
            print("Execution blocked. Use --confirm yes to proceed.")
            return

    runtime.run(
        agent_config,
        "Create workflow to mark overdue tasks urgent",
        mode=args.mode
    )


if __name__ == "__main__":
    main()
