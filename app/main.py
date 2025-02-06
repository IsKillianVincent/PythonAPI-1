from fastapi import FastAPI
from app.routes.conversion_route import router
from app.middlewares.api_key_middleware import api_key_middleware
from app.middlewares import register_middlewares

app = FastAPI(title="Currency Converter API", version="1.0")

register_middlewares(app)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)