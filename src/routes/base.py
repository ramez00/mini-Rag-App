from fastapi import FastAPI , APIRouter , Depends
from helpers.config import get_settings , Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(settings: Settings = Depends(get_settings)):
    app_name = settings.app_name
    app_version = settings.app_version
    return {
        "message": "Welcome to the application!",
        "app_name": app_name,
        "app_version": app_version
    }
    