from pydantic import BaseModel
from typing import Dict


class IcebergStats(BaseModel):
    stats: Dict[str, str]
    timeline: Dict[str, Dict[str, str]]
    properties: Dict[str, str]
