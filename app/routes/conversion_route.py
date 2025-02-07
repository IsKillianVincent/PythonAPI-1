from fastapi import APIRouter, HTTPException, Request
from app.services.exchange_service import fetch_exchange_rate
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(tags=["Conversion de devises"])
limiter = Limiter(key_func=get_remote_address)

@limiter.limit("5/minute")
@router.get("/convert")
async def convert(request: Request, amount: float, from_currency: str = "eur", to_currency: str = "usd", date: str = "latest"):
    rate = await fetch_exchange_rate(from_currency.lower(), to_currency.lower(), date)
    converted_amount = round(amount * rate, 2)

    return {
        "amount": amount,
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "date": date,
        "exchange_rate": rate,
        "converted_amount": converted_amount
    }
