import redis
from fastapi import HTTPException
import httpx
from app.configs.api_config import API_BASE_URL, API_FALLBACK_URL, API_VERSION
from app.configs.redis_config import REDIS_CACHE_EXPIRATION_TIME
from app.configs.redis_config import redis_client

async def fetch_exchange_rate(base_currency: str, target_currency: str, date: str = "latest"):
    cache_key = f"{base_currency}_{target_currency}_{date}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return float(cached_data)
    
    url = f"{API_BASE_URL}{date}/{API_VERSION}/currencies/{base_currency}.json"
    fallback_url = f"{API_FALLBACK_URL}{date}/{API_VERSION}/currencies/{base_currency}.json"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                response = await client.get(fallback_url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="La devise de référence n'existe pas")

            data = response.json().get(base_currency.lower(), {})
            rate = data.get(target_currency.lower())
            if rate is None:
                raise HTTPException(status_code=400, detail="La devise de référence n'existe pas")

            redis_client.setex(cache_key, REDIS_CACHE_EXPIRATION_TIME, rate)
            return rate
    
        data = response.json().get(base_currency.lower(), {})
        rate = data.get(target_currency.lower())
        if rate is None:
            raise HTTPException(status_code=400, detail="La devise de référence n'existe pas")
            
        redis_client.setex(cache_key, REDIS_CACHE_EXPIRATION_TIME, rate)
        return rate
    except httpx.RequestError as e:
        print('1')
        raise HTTPException(status_code=500, detail=f"Erreur de requête vers l'API: {str(e)}")
    except httpx.TimeoutException:
        print('2')
        raise HTTPException(status_code=500, detail="La requête à l'API a expiré.")
    except Exception as e:
        print('3')
        raise HTTPException(status_code=404, detail=f"Erreur inconnue lors de la récupération des taux: {str(e)}")

