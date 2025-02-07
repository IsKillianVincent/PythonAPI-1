from pydantic import BaseModel, Field
from typing import List, Optional

class ConversionRequest(BaseModel):
    amounts: List[float] = Field(..., min_items=1, description="Liste des montants à convertir")
    from_currency: str = Field(default="EUR", min_length=3, max_length=3, description="Devise source (ex: EUR)")
    to_currency: str = Field(default="USD", min_length=3, max_length=3, description="Devise cible (ex: USD)")
    date: Optional[str] = Field(default="latest", description="Date du taux de conversion")

class ConversionResponse(BaseModel):
    amount: float = Field(..., description="Montant converti")
    converted_amount: float = Field(..., description="Montant après conversion")

class ConversionResult(BaseModel):
    from_currency: str = Field(..., description="Devise source")
    to_currency: str = Field(..., description="Devise cible")
    date: str = Field(..., description="Date du taux de conversion utilisé")
    exchange_rate: float = Field(..., description="Taux de conversion appliqué")
    conversions: List[ConversionResponse] = Field(..., description="Liste des conversions effectuées")