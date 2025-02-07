import redis
from fastapi import HTTPException
import httpx
from app.configs.api_config import API_BASE_URL, API_FALLBACK_URL, API_VERSION
from app.configs.redis_config import redis_client, get_redis_cache_expiration_time
from app.exceptions.redis_exceptions import RedisConnectionError, RedisTimeoutError, RedisUnknownError

async def fetch_all_currencies():
    url = f"{API_BASE_URL}latest/v1/currencies.json"
    print(url)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                for currency, rate in data.items():
                    cache_key = f"currency_{currency}"
                    redis_client.setex(cache_key, get_redis_cache_expiration_time(), rate)
            else:
                raise Exception(f"Failed to fetch currencies: {response.status_code}")
    except Exception as e:
        print(f"Error while fetching all currencies: {str(e)}")

async def fetch_exchange_rate(base_currency: str, target_currency: str, date: str = "latest"):
    base_cache_key = f"currency_{base_currency}"
    target_cache_key = f"currency_{target_currency}"
    
    base_currency_rate = redis_client.get(base_cache_key)
    target_currency_rate = redis_client.get(target_cache_key)
    
    if not base_currency_rate:
        raise HTTPException(status_code=404, detail=f"La devise de référence {base_currency} n'existe pas.")
    
    if not target_currency_rate:
        raise HTTPException(status_code=404, detail=f"La devise cible {target_currency} n'existe pas.")
    
    cache_key = f"exchange_{base_currency}_{target_currency}_{date}"
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
                raise HTTPException(status_code=422, detail="La devise cible est invalide.")

            redis_client.setex(cache_key, get_redis_cache_expiration_time(), rate)
            return rate
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Erreur de requête vers l'API: {str(e)}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="La requête à l'API a expiré.")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur inconnue lors de la récupération des taux: {str(e)}")

