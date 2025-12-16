from app.utils.logging_handler import CustomLogger
from fastapi import APIRouter
from fastapi.requests import Request


logger = CustomLogger.get_logger(__name__)
logger.info("Router module loaded successfully.")



api_router = APIRouter()


@api_router.get("/health")
async def health_check():
    logger.info("Health check endpoint called.")
    return {"status": "healthy"}


@api_router.post("/receiveMessages")
async def receive_messages(payload: Request):
    try:
        
        logger.info("receive_messages endpoint called.")
        logger.critical("Payload received:", payload)
        return {"status": "received"}
    
    except Exception as exec:
        
        logger.error(f"Error in receive_messages endpoint: {exec}", exc_info=True)
        return {"status": "error", "message": str(exec)}



