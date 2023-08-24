from typing import Optional, Dict
from pydantic import BaseModel


class HttpDepot(BaseModel):
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    queryParams: Optional[Dict[str, str]]
