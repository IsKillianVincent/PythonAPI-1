import os
import redis

def check_redis_connection():
    try:
        redis_client = redis.StrictRedis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT", 6379),
            db=0,
            socket_timeout=5
        )
        redis_client.ping()
        return "Active"
    except redis.exceptions.ConnectionError:
        return "Inactive"
