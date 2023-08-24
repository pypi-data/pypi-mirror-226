from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field

class Oracle(BaseModel):
    url: Optional[str]
    host: Optional[str]
    port: Optional[int]
    table: Optional[str]
    service: Optional[str]
    schema_: Optional[str] = Field(alias="schema")
    subprotocol: Optional[str]
