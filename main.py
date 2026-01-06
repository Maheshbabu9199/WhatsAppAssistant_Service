from fastapi import FastAPI
from app.router.router import api_router    
from app.utils.logging_handler import CustomLogger  
from app.utils.db_handler import DBHandler
from dotenv import load_dotenv
import os 

load_dotenv()


app = FastAPI(title="WhatsApp Assistant Service", version="1.0.0")
app.include_router(api_router, prefix="/api/v1")

logger = CustomLogger.get_logger(__name__)
logger.info("WhatsApp Assistant Service has started successfully.")



@app.get("/")
async def root():
    return {"message": "Welcome to the WhatsApp Assistant Service API!"}    




@app.on_event("startup")
async def startup_event():
    
    app.state.db_handler = DBHandler(
        conn_string=os.getenv("MONGODB_CONNECTION_STRING", ""),
        database_name="WhatsApp"
    )

    await app.state.db_handler.connection.admin.command('ping')
    logger.critical("Connected to MongoDB successfully.")



@app.on_event("shutdown")
async def shutdown_event():
    
    await app.state.db_handler.connection.close()
    logger.info("WhatsApp Assistant Service has shut down successfully.")
