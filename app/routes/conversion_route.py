from fastapi import APIRouter, HTTPException, Request, Depends, Query
from app.services.exchange_service import fetch_exchange_rate
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Modèle Pydantic pour l'endpoint /convert
class ConvertQueryParams(BaseModel):
    amount: float = Field(..., description="Montant à convertir")
    from_currency: str = Field("eur", description="Devise de départ")
    to_currency: str = Field("usd", description="Devise de destination")
    date: str = Field("latest", description="Date de conversion")

@limiter.limit("5/minute")
@router.get("/convert", tags=["Conversion de devises"])
async def convert(
    request: Request,
    params: ConvertQueryParams = Depends()
):
    rate = await fetch_exchange_rate(
        params.from_currency.lower(), 
        params.to_currency.lower(), 
        params.date
    )
    converted_amount = round(params.amount * rate, 2)

    return {
        "amount": params.amount,
        "from": params.from_currency.upper(),
        "to": params.to_currency.upper(),
        "date": params.date,
        "exchange_rate": rate,
        "converted_amount": converted_amount
    }



@limiter.limit("5/minute")
@router.get("/converts")
async def converts(
    request: Request,
    amounts: List[float] = Query(..., description="Liste des montants à convertir"),
    from_currency: str = "eur",
    to_currency: str = "usd",
    date: str = "latest"
):
    rate = await fetch_exchange_rate(from_currency.lower(), to_currency.lower(), date)
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