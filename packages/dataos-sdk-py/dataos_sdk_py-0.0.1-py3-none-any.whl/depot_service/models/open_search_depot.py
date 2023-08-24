from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class OpenSearchDepot(BaseModel):
    nodes: Optional[List[str]]
    params: Optional[Dict[str, Any]]
