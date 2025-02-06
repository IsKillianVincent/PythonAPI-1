from fastapi import Request, HTTPException
from app.config import API_KEY

async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return await call_next(request)