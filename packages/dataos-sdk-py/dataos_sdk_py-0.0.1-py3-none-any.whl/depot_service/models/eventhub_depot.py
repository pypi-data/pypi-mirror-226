from typing import Optional, Dict, Any
from pydantic import BaseModel


class EventhubDepot(BaseModel):
    endpoint: Optional[str]
    params: Optional[Dict[str, Any]]
