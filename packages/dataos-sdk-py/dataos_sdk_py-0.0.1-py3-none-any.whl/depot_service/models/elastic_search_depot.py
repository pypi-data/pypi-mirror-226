from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ElasticSearchDepot(BaseModel):
    nodes: Optional[List[str]]
    params: Optional[Dict[str, Any]]
