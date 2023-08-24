from typing import Optional, Dict, Any
from pydantic import BaseModel
from pydantic.fields import Field


class Jdbc(BaseModel):
    url: Optional[str]
    table: Optional[str]
    database: Optional[str]
    host: Optional[str]
    port: Optional[int]
    subprotocol: Optional[str]
    schema_: Optional[str] = Field(alias="schema")
    params: Optional[Dict[str, Any]]
