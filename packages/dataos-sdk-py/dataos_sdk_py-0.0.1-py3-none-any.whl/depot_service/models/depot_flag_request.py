from typing import Optional
from pydantic import BaseModel


class DepotFlagRequest(BaseModel):
    isArchived: bool
    archivalMessage: Optional[str]
