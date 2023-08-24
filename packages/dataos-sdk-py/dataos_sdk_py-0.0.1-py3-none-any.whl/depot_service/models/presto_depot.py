from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PrestoDepot(BaseModel):
    host: Optional[str]
    port: Optional[int]
    catalog: Optional[str]
    schema_: Optional[str] = Field(alias="schema")
    params: Optional[Dict[str, Any]]
