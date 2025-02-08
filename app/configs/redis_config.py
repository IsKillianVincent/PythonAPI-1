import redis
from app.exceptions.redis_exceptions import RedisConnectionError, RedisTimeoutError, RedisUnknownError
import os
from dotenv import load_dotenv

load_dotenv() 

def get_redis_client():
    return redis.StrictRedis(
        host=os.getenv("REDIS_HOST", "redis-cache"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=0,
        decode_responses=True,
        socket_timeout=5
    )

redis_client = get_redis_client()

def get_redis_cache_expiration_time():
    return int(os.getenv("CACHE_EXPIRATION_TIME", 86400))

def check_redis_connection(redis_client):
    try:
        redis_client.ping()
        return "Active"
    except redis.exceptions.ConnectionError:
        raise RedisConnectionError()
    except redis.exceptions.TimeoutError:
        raise RedisTimeoutError()
    except Exception as e:
        raise RedisUnknownError(str(e))

def get_redis_cache_expiration_time(): 
    return os.getenv("CACHE_EXPIRATION_TIME", 86400)