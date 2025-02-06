import httpx
from fastapi import HTTPException
from app.config import API_BASE_URL, API_FALLBACK_URL, API_VERSION

async def fetch_exchange_rate(base_currency: str, target_currency: str, date: str = "latest"):
    url = f"{API_BASE_URL}{date}/{API_VERSION}/currencies/{base_currency}.json"
    fallback_url = f"{API_FALLBACK_URL}{date}/{API_VERSION}/currencies/{base_currency}.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            response = await client.get(fallback_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Échec de récupération des taux de change")

        data = response.json().get(base_currency.lower(), {})
        rate = data.get(target_currency.lower())
        if rate is None:
            raise HTTPException(status_code=400, detail="Devise non supportée")

        return rate