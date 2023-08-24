from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class MongoDBDepot(BaseModel):
    subprotocol: Optional[str]
    nodes: Optional[List[str]]
    params: Optional[Dict[str, Any]]
