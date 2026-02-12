from onebeam_agent_runtime.providers.openai_provider import OpenAIProvider
from onebeam_agent_runtime.providers.claude_provider import ClaudeProvider
from onebeam_agent_runtime.providers.gemini_provider import GeminiProvider

def get_model_provider(model_name):

    if model_name == "gpt-5.2":
        return OpenAIProvider()

    elif model_name == "claude-opus-4.6":
        return ClaudeProvider()

    elif model_name == "gemini-3":
        return GeminiProvider()

    else:
        raise Exception("Unsupported model")
