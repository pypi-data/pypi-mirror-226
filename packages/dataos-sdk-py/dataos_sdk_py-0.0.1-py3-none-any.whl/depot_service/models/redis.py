from typing import Optional
from pydantic import BaseModel


class Redis(BaseModel):
    host: Optional[str]
    port: Optional[int]
    table: Optional[str]
    db: Optional[int]
