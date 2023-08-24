from typing import Optional
from pydantic import BaseModel


class PulsarRequest(BaseModel):
    partitions: Optional[int]
    type: Optional[str]
