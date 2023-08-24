from typing import Optional
from pydantic import BaseModel


class Eventhub(BaseModel):
    endpoint: Optional[str]
    eventhubName: Optional[str]
