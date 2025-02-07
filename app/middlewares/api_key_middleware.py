from fastapi import Request, HTTPException
from app.config.api_config import API_KEY

async def api_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
        return await call_next(request)

    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return await call_next(request)