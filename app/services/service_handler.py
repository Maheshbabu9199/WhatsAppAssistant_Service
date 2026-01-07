import opik

from app.config.datamodels import MessageRequest
from app.services.llm_services.llms_manager import LLMsManager
from app.utils.logging_handler import CustomLogger

opik_client = opik.Opik()

logger = CustomLogger.get_logger(__name__)


class ServiceHandler:
    def __init__(self, db_handler) -> None:
        self.db_handler = db_handler
        self.llms_manager: LLMsManager = LLMsManager()

    async def process_incoming_message(self, message_request: MessageRequest):
        try:
            logger.info(f"Processing incoming message id: {message_request.message_id}")

            response = await self.llms_manager.generate_response(
                user_id=message_request.sender_id,
                user_message=message_request.message,
            )

            return response

        except Exception as exec:
            logger.error(f"Error in process_incoming_message: {exec}", exc_info=True)
            raise exec
