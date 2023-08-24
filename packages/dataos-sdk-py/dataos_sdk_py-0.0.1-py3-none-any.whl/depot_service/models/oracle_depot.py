from typing import Optional, Dict, Any
from pydantic import BaseModel


class OracleDepot(BaseModel):
    subprotocol: Optional[str]
    host: Optional[str]
    port: Optional[int]
    service: Optional[str]
    params: Optional[Dict[str, Any]]
