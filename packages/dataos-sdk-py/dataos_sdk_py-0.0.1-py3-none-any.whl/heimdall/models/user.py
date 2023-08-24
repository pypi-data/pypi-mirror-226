from typing import List

from pydantic import BaseModel
from pydantic.fields import Optional, Dict, Field

from heimdall.models.links import Links


class User(BaseModel):
    name: str
    type: str
    id: str
    email: str
    cid: str
    properties: Optional[List[Dict]]
    federated_user_id: Optional[str]
    federated_connector_id: Optional[str]
    tags: Optional[List[str]]
    links: Links = Field(alias="_links")
