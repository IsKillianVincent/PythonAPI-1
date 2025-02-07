from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app.routes.conversion_route import router as conversion_router
from app.routes.config_route import router as config_router
from app.middlewares import register_middlewares
from app.config.redis_config import redis_client
import redis
from slowapi import Limiter
from slowapi.util import get_remote_address

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="API de conversion de devises",
    version="1.0",
    description="Une API pour convertir des devises",
    openapi_version="3.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json", 
)

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


@app.on_event("startup")
async def startup_event():
    try:
        redis_client.ping()
        print("Connexion Redis réussie.")
    except redis.ConnectionError:
        print("Connexion Redis a échoué.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)