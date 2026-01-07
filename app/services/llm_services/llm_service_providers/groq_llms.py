import os

import opik
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from opik.integrations.langchain import OpikTracer

from app.services.llm_services.llm_service_providers.llms_interface import LLMService
from app.utils.logging_handler import CustomLogger

load_dotenv()


logger = CustomLogger.get_logger(__name__)

opik_tracer = OpikTracer(
    project_name="WhatsApp Service",
    tags=["groq"],
    metadata={"service": "whatsapp-assistant-service"},
)

opik_client = opik.Opik()


class GroqLLMService(LLMService):
    def __init__(self) -> None:
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model_name = os.getenv("GROQ_MODEL_NAME", "qwen/qwen3-32b")
        self.client = ChatGroq(
            api_key=self.api_key,
            model_name=self.model_name,
            temperature=0.7,
            max_tokens=200,
            reasoning_format="parsed",
        )

    async def generate_response(self, chat_prompt: list, user_id: str) -> str:
        """
        Generate a response from the Groq LLM based on user input.

        """

        try:
            logger.info(f"Generating response from Groq LLM for user_id: {user_id}")
            response = await self.client.ainvoke(
                input=chat_prompt,
                config={
                    "callbacks": [opik_tracer],
                    "configurable": {"thread_id": user_id},
                },
            )

            return response.content

        except Exception as exec:
            logger.error(
                f"Error in GroqLLMService generate_response: {exec}",
                exc_info=True,
            )
            raise exec
