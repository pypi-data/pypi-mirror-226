from typing import Optional, Dict, Any
from pydantic import BaseModel


class PulsarDepot(BaseModel):
    adminUrl: Optional[str]
    serviceUrl: Optional[str]
    tenant: Optional[str]
    params: Optional[Dict[str, Any]]
