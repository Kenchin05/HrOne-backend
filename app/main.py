from fastapi import FastAPI
from .routes import router as api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the HROne Backend API!"}