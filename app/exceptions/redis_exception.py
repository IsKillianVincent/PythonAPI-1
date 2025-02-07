from redis.exceptions import ConnectionError, TimeoutError

def redis_connection_error():
    try:
        redis_client.ping()
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Erreur de connexion à Redis. Vérifiez votre connexion réseau.")
    except TimeoutError:
        raise HTTPException(status_code=500, detail="Le délai de connexion à Redis a expiré.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue avec Redis: {str(e)}")
