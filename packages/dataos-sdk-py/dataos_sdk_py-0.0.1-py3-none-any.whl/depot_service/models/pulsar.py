from typing import Optional, Dict, Any
from pydantic import BaseModel


class Pulsar(BaseModel):
    serviceUrl: Optional[str]
    adminUrl: Optional[str]
    tenant: Optional[str]
    topic: Optional[str]
    isPersistent: Optional[bool]
    params: Optional[Dict[str, Any]]
