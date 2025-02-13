from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app.routes.conversion_route import router as conversion_router
from app.routes.config_route import router as config_router
from app.middlewares import register_middlewares
from app.configs.redis_config import redis_client
import redis
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI
from app.exceptions.http_exceptions import http_exception_handler
from app.exceptions.validation_exceptions import validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.exchange_service import fetch_all_currencies
from fastapi import FastAPI, HTTPException
from app.configs.redis_config import get_redis_client, check_redis_connection
from app.exceptions.redis_exceptions import RedisConnectionError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="API de conversion de devises",
    version="1.0",
    description="Une API pour convertir des devises",
    openapi_version="3.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json", 
)

app.state.limiter = limiter

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

register_middlewares(app)
app.include_router(conversion_router)
app.include_router(config_router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.on_event("startup")
async def startup_event():
    
    redis_client = get_redis_client()
    try:
        connection_status = check_redis_connection(redis_client)
        print(f"Redis connection: {connection_status}")
        scheduler = AsyncIOScheduler()
        scheduler.add_job(fetch_all_currencies, IntervalTrigger(hours=24))
        scheduler.start()
        await fetch_all_currencies()
    except RedisConnectionError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except RedisTimeoutError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except RedisUnknownError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)