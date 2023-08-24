from typing import Optional, Dict, Any
from pydantic import BaseModel


class MysqlDepot(BaseModel):
    subprotocol: Optional[str]
    host: Optional[str]
    port: Optional[int]
    params: Optional[Dict[str, Any]]
