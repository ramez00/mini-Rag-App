from fastapi import FastAPI , APIRouter
from helpers.config import get_settings

settings = get_settings()

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome():
    app_name = settings.app_name
    app_version = settings.app_version
    return {
        "message": "Welcome to the application!",
        "app_name": app_name,
        "app_version": app_version
    }
    