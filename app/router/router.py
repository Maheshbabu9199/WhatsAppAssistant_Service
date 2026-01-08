from typing import cast
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from app.config.datamodels import MessageRequest
from app.services.service_handler import ServiceHandler
from app.utils.db_handler import DBHandler
from app.utils.logging_handler import CustomLogger
import cProfile
import time

logger = CustomLogger.get_logger(__name__)

logger.info("Router module loaded successfully.")


class AppState:
    db_handler: DBHandler
    service_handler: ServiceHandler


profiler = cProfile.Profile()
profiler.enable()
api_router = APIRouter()


@api_router.get("/health")
async def health_check():
    logger.info("Health check endpoint called.")
    return ORJSONResponse(content={"status": "healthy"}, status_code=200)


@api_router.route("/webhook", methods=["POST", "GET"])
async def receive_messages(payload: Request):
    try:
        logger.info("receive_messages endpoint called.")
        logger.critical(f"Payload received: {payload}")

        app_state = cast(AppState, payload.app.state)
        body = await payload.form()
        start_time = time.time()

        message_request = MessageRequest(
            profilename=body.get("ProfileName"),
            sender_id=body.get("WaId"),
            message=body.get("Body"),
            message_type=body.get("MessageType"),
            message_id=body.get("MessageSid"),
        )

        logger.critical(f"Message request data: {message_request}")

        reply_message = await app_state.service_handler.process_incoming_message(
            message_request
        )
        profiler.disable()

        # s = io.StringIO()
        # stats = pstats.Stats(profiler, stream=s)
        # stats.sort_stats("cumulative")
        # stats.print_stats(30)

        # print(s.getvalue())

        logger.critical(f"Reply message generated: {reply_message}")

        logger.warning(f"TOTAL TIME TAKEN: {time.time() - start_time} seconds")
        return ORJSONResponse(
            content={"status": "success", "body": reply_message},
            status_code=200,
        )

    except Exception as exec:
        logger.error(f"Error in receive_messages endpoint: {exec}", exc_info=True)
        return {"status": "error", "message": str(exec)}
