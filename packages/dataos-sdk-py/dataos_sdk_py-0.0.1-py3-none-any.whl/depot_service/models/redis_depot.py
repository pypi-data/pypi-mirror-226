from typing import Optional
from pydantic import BaseModel


class RedisDepot(BaseModel):
    host: Optional[str]
    port: Optional[int]
    db: Optional[int]
