from fastapi import APIRouter, Query, HTTPException, Request, Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List
from app.models.conversion_model import ConvertQueryParams, ConvertsQueryParams
from app.services.exchange_service import fetch_exchange_rate

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("2/minute")
@router.post("/convert", tags=["Conversion de devises"])
async def convert(request: Request, params: ConvertQueryParams):
    """
    Convertit un montant d'une devise vers une autre.
    """
    try:
        rate = await fetch_exchange_rate(params.from_currency, params.to_currency, params.date)
    except RateLimitExceeded:
        raise HTTPException(
            status_code=429,
            detail="Limite de requêtes atteinte. Veuillez réessayer dans 60 secondes."
        )

    converted_amount = round(params.amount * rate, 2)

    return {
        "amount": params.amount,
        "from": params.from_currency,
        "to": params.to_currency,
        "date": params.date,
        "exchange_rate": rate,
        "converted_amount": converted_amount
    }

@limiter.limit("2/minute") 
@router.post("/converts", tags=["Conversion multiple"])
async def converts(request: Request, params: ConvertsQueryParams):
    print(Request)
    print(ConvertsQueryParams)
    """
    Convertit plusieurs montants d'une devise vers une autre.
    """
    try:
        rate = await fetch_exchange_rate(params.from_currency, params.to_currency, params.date)
    except RateLimitExceeded:
        raise HTTPException(
            status_code=429,
            detail="Limite de requêtes atteinte. Veuillez réessayer dans 60 secondes."
        )

    conversions = [
        {
            "amount": amount,
            "converted_amount": round(amount * rate, 2)
        }
        for amount in params.amounts
    ]

    return {
        "from": params.from_currency,
        "to": params.to_currency,
        "date": params.date,
        "exchange_rate": rate,
        "conversions": conversions
    }