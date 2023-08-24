from typing import Optional, Dict, Any
from pydantic import BaseModel


class SnowflakeDepot(BaseModel):
    url: Optional[str]
    database: Optional[str]
    warehouse: Optional[str]
    params: Optional[Dict[str, Any]]
