from fastapi import Request, HTTPException
from app.configs.api_config import API_KEY

async def api_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
        return await call_next(request)

    api_key = request.headers.get("Authorization")
    if not api_key or not api_key.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Clé d'API manquante ou mal formée")
    
    token = api_key.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Accès non autorisé avec cette clé d'API")
    
    return await call_next(request)
