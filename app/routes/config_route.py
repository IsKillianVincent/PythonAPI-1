from fastapi import APIRouter, HTTPException
import os
import time
from dotenv import load_dotenv
from app.configs.redis_config import redis_client, check_redis_connection
import redis

load_dotenv()

router = APIRouter(tags=["Configuration - Gestion du cache"])

@router.get("/config", include_in_schema=False)
async def get_config():
    start_time = time.time()

    try:
        external_api_info = {
            "API_VERSION": os.getenv("API_VERSION", "1.0"),
            "API_BASE_URL": os.getenv("API_BASE_URL", ""),
            "API_FALLBACK_URL": os.getenv("API_FALLBACK_URL", ""),
        }

        internal_api_info = {
            "APP_VERSION": os.getenv("APP_VERSION", "1.0"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
            "PROJECT_PATH": os.path.abspath(os.getcwd()),
            "DEBUG_MODE": os.getenv("DEBUG", "False"),
            "API_KEY_PRESENT": bool(os.getenv("API_KEY")),
            "DATABASE_CONNECTION": "Active" if os.getenv("DATABASE_URL") else "Inactive",
            "UPTIME": round(time.time() - start_time, 2)
        }

        redis_info = {
            "REDIS_CONNECTION": check_redis_connection(redis_client),
            "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
            "REDIS_PORT": os.getenv("REDIS_PORT", 6379)
        }

        return {
            "external_api_info": external_api_info,
            "internal_api_info": internal_api_info,
            "redis_info": redis_info
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching configuration: {str(e)}")

@router.get("/cache/stats")
async def get_cache_stats():
    try:
        stats = redis_client.info()
        if stats.get("db0") is None:
            raise HTTPException(status_code=500, detail="Unable to fetch Redis DB stats")

        return {
            "keys_count": stats.get("db0", {}).get("keys", 0),
            "memory_used": stats.get("used_memory_human", "N/A"),
            "uptime": stats.get("uptime_in_seconds", 0),
        }
    except redis.exceptions.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cache stats: {str(e)}")

@router.get("/cache/keys")
async def get_cache_keys():
    try:
        keys = redis_client.keys("*")
        return {"keys": keys}
    except redis.exceptions.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cache keys: {str(e)}")

@router.delete("/cache/{key}")
async def delete_cache_key(key: str):
    try:
        deleted = redis_client.delete(key)
        if deleted:
            return {"message": f"Key '{key}' successfully deleted."}
        else:
            raise HTTPException(status_code=404, detail=f"Key '{key}' not found.")
    except redis.exceptions.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting cache key: {str(e)}")
