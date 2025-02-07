import redis
from fastapi import HTTPException
import httpx
from app.config.api_config import API_BASE_URL, API_FALLBACK_URL, API_VERSION
from app.config.redis_config import REDIS_CACHE_EXPIRATION_TIME
from app.config.redis_config import redis_client

async def fetch_exchange_rate(base_currency: str, target_currency: str, date: str = "latest"):
    cache_key = f"{base_currency}_{target_currency}_{date}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        print(f"Sauvegarde de cache pour {cache_key}")
        return float(cached_data)

    print(f"Absence de cache pour {cache_key}. Récupération de l'API...")
    
    url = f"{API_BASE_URL}{date}/{API_VERSION}/currencies/{base_currency}.json"
    fallback_url = f"{API_FALLBACK_URL}{date}/{API_VERSION}/currencies/{base_currency}.json"

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
