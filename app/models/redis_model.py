from pydantic import BaseModel, Field
from typing import List, Optional

class CacheStatsResponse(BaseModel):
    keys_count: int = Field(..., description="Nombre de clés stockées en cache")
    memory_used: str = Field(..., description="Mémoire utilisée par Redis")
    uptime: int = Field(..., description="Durée de fonctionnement du cache en secondes")
