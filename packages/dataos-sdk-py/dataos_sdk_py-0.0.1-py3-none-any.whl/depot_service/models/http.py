from typing import Optional, Dict
from pydantic import BaseModel


class Http(BaseModel):
    url: Optional[str]
    headers: Optional[Dict[str, str]]
    queryParams: Optional[Dict[str, str]]
