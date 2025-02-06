from fastapi import FastAPI
from app.middlewares.api_key_middleware import api_key_middleware

def register_middlewares(app: FastAPI):
    app.middleware("http")(api_key_middleware)
