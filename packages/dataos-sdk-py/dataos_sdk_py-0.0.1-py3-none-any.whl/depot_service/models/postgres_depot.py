from typing import Optional, Dict, Any
from pydantic import BaseModel


class PostgresDepot(BaseModel):
    subprotocol: Optional[str]
    host: Optional[str]
    port: Optional[int]
    database: Optional[str]
    params: Optional[Dict[str, Any]]
