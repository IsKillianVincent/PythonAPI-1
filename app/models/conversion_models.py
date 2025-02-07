from pydantic import BaseModel, Field

class ConvertQueryParams(BaseModel):
    amount: float = Field(..., description="Montant à convertir")
    from_currency: str = Field("eur", description="Devise de départ")
    to_currency: str = Field("usd", description="Devise de destination")
    date: str = Field("latest", description="Date de conversion")