
from fastapi import FastAPI
from src.routers.documents import router as documents_router

app = FastAPI(title="Task-3 Knowledge Base API")

app.include_router(documents_router)
