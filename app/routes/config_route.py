from fastapi import APIRouter
import os
import time
from app.config import API_VERSION, API_BASE_URL, API_FALLBACK_URL
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/config", include_in_schema=False)
async def get_config():
    start_time = time.time()

    external_api_info = {
        "API_VERSION": API_VERSION,
        "API_BASE_URL": API_BASE_URL,
        "API_FALLBACK_URL": API_FALLBACK_URL,
    }

    internal_api_info = {
        "APP_VERSION": "1.0",
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
        "PROJECT_PATH": os.path.abspath(os.getcwd()),
        "DEBUG_MODE": os.getenv("DEBUG", "False"),
        "API_KEY_PRESENT": bool(os.getenv("API_KEY")),
        "DATABASE_CONNECTION": "Active" if os.getenv("DATABASE_URL") else "Inactive",
        "UPTIME": round(time.time() - start_time, 2)
    }

    return {
        "external_api_info": external_api_info,
        "interal_api_info": internal_api_info
    }
