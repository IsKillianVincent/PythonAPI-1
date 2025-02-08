from pydantic import BaseModel, Field, validator, constr
from typing import List, Optional
import re
from app.configs.redis_config import redis_client

CURRENCY_REGEX = re.compile(r"^[a-z]{3}$")

def is_valid_currency(currency: str) -> bool:
    """Vérifie si la devise existe dans le cache Redis (stockée en minuscule)."""
    return redis_client.exists(f"currency_{currency.lower()}") > 0

class ConvertQueryParams(BaseModel):
    amount: float = Field(..., gt=0, description="Montant à convertir (doit être strictement positif)")
    from_currency: constr(strict=True, min_length=3, max_length=3) = Field(..., description="Devise source (ISO 4217)")
    to_currency: constr(strict=True, min_length=3, max_length=3) = Field(..., description="Devise cible (ISO 4217)")
    date: str = Field("latest", description="Date de conversion (format YYYY-MM-DD ou 'latest')")

    @validator("from_currency", "to_currency")
    def validate_currency(cls, value):
        value = value.lower()
        if not CURRENCY_REGEX.match(value) or not is_valid_currency(value):
            raise ValueError(f"Devise invalide ou non supportée: {value}.")
        return value

    @validator("date")
    def validate_date(cls, value):
        if value.lower() == "latest":
            return "latest"
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            raise ValueError("Format de date invalide. Utilisez 'YYYY-MM-DD' ou 'latest'.")
        return value

class ConvertsQueryParams(BaseModel):
    amounts: List[float] = Field(..., min_items=1, description="Liste des montants à convertir (doivent être positifs)", alias="amounts", serialization_alias="amounts")
    from_currency: constr(strict=True, min_length=3, max_length=3) = Field(..., description="Devise source (ISO 4217)")
    to_currency: constr(strict=True, min_length=3, max_length=3) = Field(..., description="Devise cible (ISO 4217)")
    date: Optional[str] = Field(default="latest", description="Date du taux de conversion")

    @validator("amounts")
    def validate_amounts(cls, amounts):
        if any(amount <= 0 for amount in amounts):
            raise ValueError("All amounts must be strictly positive.")
        return amounts

    @validator("from_currency", "to_currency")
    def validate_currency(cls, value):
        value = value.lower()
        if not CURRENCY_REGEX.match(value) or not is_valid_currency(value):
            raise ValueError(f"Devise invalide ou non supportée: {value}.")
        return value

    @validator("date")
    def validate_date(cls, value):
        if value.lower() == "latest":
            return "latest"
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            raise ValueError("Format de date invalide. Utilisez 'YYYY-MM-DD' ou 'latest'.")
        return value