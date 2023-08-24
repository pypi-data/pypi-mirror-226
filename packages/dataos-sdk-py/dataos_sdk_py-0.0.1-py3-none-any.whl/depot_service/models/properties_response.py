from pydantic import BaseModel
from pydantic.fields import Dict


class PropertiesResponse(BaseModel):
    properties: Dict[str, str]
