from flask import Flask, render_template, request

from onebeam_agent_runtime.core.agent_runtime import AgentRuntime
from onebeam_agent_runtime.agents.workflow_agent import WORKFLOW_AGENT

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    output = None
    error = None

    if request.method == "POST":

        model = request.form.get("model")
        mode = request.form.get("mode")
        confirm = request.form.get("confirm")

        agent_config = WORKFLOW_AGENT.copy()
        agent_config["model"] = model

        runtime = AgentRuntime()

        if mode == "execution" and confirm != "yes":
            error = "Execution blocked. You must confirm execution."
        else:
            try:
                result = runtime.run(
                    agent_config,
                    request.form.get("user_input"),
                    mode=mode
                )
                output = result
            except Exception as e:
                error = str(e)

    return render_template("index.html", output=output, error=error)


if __name__ == "__main__":
    app.run(debug=True)
