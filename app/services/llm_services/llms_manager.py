import opik

from app.services.llm_services.llm_service_providers.groq_llms import GroqLLMService
from app.services.llm_services.llm_service_providers.llms_interface import LLMService
from app.utils.constants_retriever import ConstantsRetriever
from app.utils.custom_enums import LLMProviders, PromptNames
from app.utils.logging_handler import CustomLogger

opik_client = opik.Opik()

logger = CustomLogger.get_logger(__name__)


class LLMsManager:
    def __init__(
        self,
    ) -> None:
        self.llm_service = self.get_llm_service()

    def get_llm_service(self) -> LLMService:
        provider = ConstantsRetriever.get_constants("LLM_PROVIDER")

        match provider:
            case LLMProviders.GROQ.value:
                return GroqLLMService()

            case LLMProviders.OPENAI.value:
                return NotImplementedError("OpenAI LLM Service is not implemented yet.")

            case _:
                raise ValueError("Unsupported LLM provider")

    async def generate_response(self, user_id: str, user_message: str) -> str:
        try:
            prompt = opik_client.get_chat_prompt(
                name=PromptNames.WHATSAPP_SERVICE_CHAT_PROMPT.value
            )
            chat_prompt = prompt.format({"user_input": user_message})

            return await self.llm_service.generate_response(
                chat_prompt=chat_prompt, user_id=user_id
            )

        except Exception as exec:
            logger.error(f"Error: Reporting from llms manager: {exec}", exc_info=True)
            raise exec
