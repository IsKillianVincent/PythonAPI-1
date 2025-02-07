from fastapi import APIRouter
import os
import time
import redis
from app.config import API_VERSION, API_BASE_URL, API_FALLBACK_URL
from dotenv import load_dotenv
from app.utils.redis_util import check_redis_connection
from app.redis_config import redis_client

load_dotenv() 

router = APIRouter(tags=["Congiguration - Gestion du cache"])

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

    redis_info = {
        "REDIS_CONNECTION": check_redis_connection(),
        "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
        "REDIS_PORT": os.getenv("REDIS_PORT", 6379)
    }

    return {
        "external_api_info": external_api_info,
        "internal_api_info": internal_api_info,
        "redis_info": redis_info
    }

@router.get("/cache/stats")
async def get_cache_stats():
    try:
        stats = redis_client.info()
        return {
            "keys_count": stats.get("db0", {}).get("keys", 0),
            "memory_used": stats.get("used_memory_human", "N/A"),
            "uptime": stats.get("uptime_in_seconds", 0),
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/cache/keys")
async def get_cache_keys():
    try:
        keys = redis_client.keys("*")
        return {"keys": keys}
    except Exception as e:
        return {"error": str(e)}

@router.delete("/cache/{key}")
async def delete_cache_key(key: str):
    deleted = redis_client.delete(key)
    return {"deleted": bool(deleted)}