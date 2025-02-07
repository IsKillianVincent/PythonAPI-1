from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.configs.api_config import API_KEY

async def api_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
        return await call_next(request)

    api_key = request.headers.get("Authorization")

    if not api_key:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Accès non autorisé",
                "message": "Aucun token fourni. Ajoutez un en-tête Authorization sous la forme 'Bearer <API_KEY>'."
            }
        )

    if not api_key.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={
                "error": "Accès non autorisé",
                "message": "Format du token incorrect. Le format attendu est 'Bearer <API_KEY>'."
            }
        )

    provided_key = api_key[7:].strip()

    if provided_key != API_KEY:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Erreur",
                "message": "Erreur survenue : Token invalide. Vérifiez que votre clé API est correcte."
            }
        )

    return await call_next(request)
