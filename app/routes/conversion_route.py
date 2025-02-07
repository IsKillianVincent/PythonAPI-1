from fastapi import APIRouter, Query, HTTPException, Request, Depends
from typing import List
from app.models.conversion_model import ConversionRequest, ConversionResult
from app.services.exchange_service import fetch_exchange_rate
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@limiter.limit("2/minute")
@router.get("/convert", tags=["Conversion de devises"])
async def convert(request: Request, amount: float, from_currency: str = "eur", to_currency: str = "usd", date: str = "latest"):
    try:
        rate = await fetch_exchange_rate(from_currency.lower(), to_currency.lower(), date)
    except RateLimitExceeded as e:
        raise HTTPException(
            status_code=429,
            detail="Limite de requêtes atteinte. Veuillez réessayer dans 60 secondes."
        )
    
    converted_amount = round(amount * rate, 2)

    return {
        "amount": amount,
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "date": date,
        "exchange_rate": rate,
        "converted_amount": converted_amount
    }

@limiter.limit("2/minute")
@router.get("/converts")
async def converts(
    request: Request,
    amounts: List[float] = Query(..., description="Liste des montants à convertir"),
    from_currency: str = "eur",
    to_currency: str = "usd",
    date: str = "latest"
):
    try:
        rate = await fetch_exchange_rate(from_currency.lower(), to_currency.lower(), date)
    except RateLimitExceeded as e:
        raise HTTPException(
            status_code=429,
            detail="Limite de requêtes atteinte. Veuillez réessayer dans 60 secondes."
        )
    conversions = [
        {
            "amount": amount,
            "converted_amount": round(amount * rate, 2)
        }
        for amount in amounts
    ]

    return {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "date": date,
        "exchange_rate": rate,
        "conversions": conversions
    }