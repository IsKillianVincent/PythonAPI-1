from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Erreur survenue : {exc.detail}", "path": request.url.path}
    )