from fastapi import Request, HTTPException
from app.configs.api_config import API_KEY

async def api_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
        return await call_next(request)
    
    api_key = request.headers.get("Authorization")
    
    if api_key and api_key.startswith("Bearer "):
        api_key = api_key[len("Bearer "):]
    
    print(f"Expected: {API_KEY}, Received: {repr(api_key)}")
    
    if api_key != API_KEY:
        print(f"Bearer err: {repr(API_KEY)}, Received: {repr(api_key)}")
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    return await call_next(request)
