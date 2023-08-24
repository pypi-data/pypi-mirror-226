from typing import Optional
from pydantic import BaseModel


class PulsarResponse(BaseModel):
    partitions: Optional[int]
    type: Optional[str]
