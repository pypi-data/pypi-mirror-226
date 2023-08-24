from pydantic import BaseModel
from pydantic.fields import Optional


class MetadataVersionResponse(BaseModel):
    version: str
    timestamp: int
