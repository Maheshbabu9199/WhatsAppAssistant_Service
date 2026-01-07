import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.router.router import api_router
from app.services.service_handler import ServiceHandler
from app.utils.db_handler import DBHandler
from app.utils.logging_handler import CustomLogger

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_handler = DBHandler(
        conn_string=os.getenv("MONGODB_CONNECTION_STRING", ""),
        database_name="WhatsApp",
    )

    app.state.service_handler = ServiceHandler(app.state.db_handler)

    await app.state.db_handler.connection.admin.command("ping")
    logger.critical("Connected to MongoDB successfully.")

    yield

    await app.state.db_handler.connection.close()
    logger.info("WhatsApp Assistant Service has shut down successfully.")


app = FastAPI(title="WhatsApp Assistant Service", version="1.0.0", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")

logger = CustomLogger.get_logger(__name__)
logger.info("WhatsApp Assistant Service has started successfully.")


@app.get("/")
async def root():
    return {"message": "Welcome to the WhatsApp Assistant Service API!"}
