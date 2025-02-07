from fastapi import HTTPException

class RedisConnectionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail="Erreur de connexion à Redis. Vérifiez votre connexion réseau."
        )

class RedisTimeoutError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail="Le délai de connexion à Redis a expiré."
        )

class RedisUnknownError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=500,
            detail=f"Erreur inconnue avec Redis: {message}"
        )
