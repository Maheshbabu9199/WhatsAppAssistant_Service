from app.utils.logging_handler import CustomLogger
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from fastapi.requests import Request


logger = CustomLogger.get_logger(__name__)
logger.info("Router module loaded successfully.")



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
        app_state = payload.app.state
        body = await payload.form()
        logger.debug(f"Request body: {body}")

        return ORJSONResponse(content={"status": "success", "body": "Maheshbabu"}, status_code=200)

    except Exception as exec:
        
        logger.error(f"Error in receive_messages endpoint: {exec}", exc_info=True)
        return {"status": "error", "message": str(exec)}



