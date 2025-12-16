from fastapi import FastAPI
from app.router.router import api_router    



app = FastAPI(title="WhatsApp Assistant Service", version="1.0.0")
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to the WhatsApp Assistant Service API!"}    


