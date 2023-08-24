from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class Presto(BaseModel):
    url: Optional[str]
    host: Optional[str]
    port: Optional[int]
    catalog: Optional[str]
    schema_: Optional[str]= Field(alias="schema")
