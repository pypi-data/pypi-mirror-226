from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class MongoDb(BaseModel):
    connectionUrl: Optional[str]
    subprotocol: Optional[str]
    nodes: Optional[List[str]]
    database: Optional[str]
    table: Optional[str]
    params: Optional[Dict[str, Any]]
