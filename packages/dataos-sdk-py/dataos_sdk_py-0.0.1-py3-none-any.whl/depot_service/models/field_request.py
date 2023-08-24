from pydantic import BaseModel
from pydantic.fields import Optional


class FieldRequest(BaseModel):
    name: str
    type: str
    precision: Optional[int]
    scale: Optional[int]
    keyType: Optional[str]
    valueType: Optional[str]
