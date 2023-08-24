from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class Kafka(BaseModel):
    brokers: Optional[List[str]]
    topic: Optional[str]
    schemaRegistryUrl: Optional[str]
    params: Optional[Dict[str, Any]]
