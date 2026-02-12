from abc import ABC, abstractmethod

class LLMProvider(ABC):

    @abstractmethod
    def generate_structured_output(self, system_prompt, user_prompt, tools, output_schema):
        pass
