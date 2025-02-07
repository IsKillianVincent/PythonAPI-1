from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
async def validation_exception_handler(request, exc: RequestValidationError):
    details = [{"field": error['loc'], "message": error['msg']} for error in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"message": "Erreur de validation des données", "details": details}
    )