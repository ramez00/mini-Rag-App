from ..LLMInterface import LLMInterface
from ..LLMEnums import AnthropicEnums
from anthropic import Anthropic
import logging


class AnthropicProvider(LLMInterface):

    def __init__(self, api_key: str,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):

        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        # Claude has no embedding model; keep embeddings on Cohere/OpenAI/etc.
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = Anthropic(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)
        self.enums = AnthropicEnums

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = None,
                      max_output_tokens: int = None, temperature: float = None):

        if not self.client:
            self.logger.error("Anthropic client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for Anthropic was not set")
            return None

        max_output_tokens = (max_output_tokens if max_output_tokens is not None
                             else self.default_generation_max_output_tokens)
        temperature = (temperature if temperature is not None
                       else self.default_generation_temperature)

        # Fresh copy every call (never mutate a shared default list)
        history = list(chat_history) if chat_history else []
        history.append(self.construct_prompt(prompt=prompt, role=AnthropicEnums.USER.value))

        # Claude takes the system prompt as a separate parameter,
        # and `messages` may only contain "user" / "assistant" roles.
        system_parts = [m["content"] for m in history if m["role"] == AnthropicEnums.SYSTEM.value]
        messages = [m for m in history if m["role"] != AnthropicEnums.SYSTEM.value]

        request = {
            "model": self.generation_model_id,
            "max_tokens": max_output_tokens,
            "messages": messages,
            "temperature": temperature,
        }
        if system_parts:
            request["system"] = "\n".join(system_parts)

        try:
            response = self.client.messages.create(**request)
        except Exception as e:
            self.logger.error(f"Error while generating text with Anthropic: {e}")
            return None

        # The response is a list of content blocks; keep only the text ones
        text_blocks = [block.text for block in response.content if block.type == "text"]
        if not text_blocks:
            self.logger.error("Anthropic returned no text content")
            return None

        return "".join(text_blocks)

    def embed_text(self, text: str, document_type: str = None):
        self.logger.error("Anthropic does not provide embeddings; use another EMBEDDING_BACKEND")
        return None

    def construct_prompt(self, prompt: str, role: str):
        # No truncation here: RAG prompts carry the retrieved chunks
        return {
            "role": role,
            "content": prompt,
        }