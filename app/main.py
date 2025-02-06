from fastapi import FastAPI
from app.routes.conversion_route import router as conversion_router
from app.routes.config_route import router as config_router
from app.middlewares.api_key_middleware import api_key_middleware
from app.middlewares import register_middlewares

app = FastAPI(title="Currency Converter API", version="1.0")

register_middlewares(app)

app.include_router(conversion_router)
app.include_router(config_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)