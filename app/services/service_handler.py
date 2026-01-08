import opik
from app.config.datamodels import MessageRequest
from app.utils.db_handler import DBHandler
from app.services.llm_services.llms_manager import LLMsManager
from app.utils.logging_handler import CustomLogger
from datetime import datetime
import asyncio
from langchain_core.messages.ai import AIMessage

opik_client = opik.Opik()

logger = CustomLogger.get_logger(__name__)


class ServiceHandler:
    def __init__(self, db_handler) -> None:
        self.db_handler: DBHandler = db_handler
        self.llms_manager: LLMsManager = LLMsManager()

    async def process_incoming_message(self, message_request: MessageRequest):
        try:
            logger.info(f"Processing incoming message id: {message_request.message_id}")
            response = None

            response: AIMessage = await self.llms_manager.generate_response(
                user_id=message_request.sender_id,
                user_message=message_request.message,
            )

            return response.content

        except Exception as exec:
            logger.error(f"Error in process_incoming_message: {exec}", exc_info=True)
            raise exec

        finally:
            await asyncio.gather(
                self.save_user_info(message_request),
                self.save_message_interaction(message_request, response),
            )

    async def save_message_interaction(
        self, message_request: MessageRequest, response: str
    ):
        """
        saving the interaction to the database
        """
        try:
            logger.info(
                f"saving message interaction for user_id: {message_request.sender_id}"
            )

            if not response:
                # when no response from the llms
                response = AIMessage(content="")

            session_info = {
                "user_id": message_request.sender_id,
                "message_id": message_request.message_id,
                "message_type": message_request.message_type,
                "message": message_request.message,
                "response": response.__dict__,
                "created_at": datetime.now(),
            }

            await self.db_handler.insertDocs(
                collection_name="SessionsInfo", data=[session_info]
            )
            logger.critical(
                f"Message interaction saved for user_id: {message_request.sender_id}"
            )

        except Exception as exec:
            logger.error(f"Error in saving the message: {exec}", exc_info=True)
            raise exec

    async def save_user_info(self, message_request: MessageRequest):
        """
        saving user info to the database

        """

        try:
            logger.info(f"saving user info for user_id: {message_request.sender_id}")

            user_info = {
                "user_id": message_request.sender_id,
                "user_name": message_request.profilename,
                "last_interaction": datetime.now(),
            }

            existing_user = await self.db_handler.updateDocs(
                collection_name="UsersInfo",
                query={"user_id": message_request.sender_id},
                new_values=user_info,
            )

            print(f"Existing user: {existing_user}")
            if not existing_user:
                await self.db_handler.insertDocs(
                    collection_name="UsersInfo", data=[user_info]
                )

            logger.critical(
                f"User info saved/updated for user_id: {message_request.sender_id}"
            )

        except Exception as exec:
            logger.error(f"Error in saving the user info: {exec}", exc_info=True)
            raise exec
