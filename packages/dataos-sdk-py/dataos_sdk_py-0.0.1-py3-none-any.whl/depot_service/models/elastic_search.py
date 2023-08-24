from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ElasticSearch(BaseModel):
    nodes: Optional[List[str]]
    index: Optional[str]
    type: Optional[str]
    params: Optional[Dict[str, Any]]
