from pydantic import BaseModel
from pydantic.fields import Optional


class FieldUpdateRequest(BaseModel):
    type: str
    precision: Optional[int]
    scale: Optional[int]
