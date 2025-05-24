from fastapi import APIRouter
from helpers.config import get_settings


base_router = APIRouter(
    prefix = "/api/v1",
    tags = ["api_v1"]
)

@base_router.get("/")
async def welcome():
    app_setting = get_settings()
    return {
        "app_name": app_setting.APP_NAME,
        "app_version": app_setting.APP_VERSION
    }