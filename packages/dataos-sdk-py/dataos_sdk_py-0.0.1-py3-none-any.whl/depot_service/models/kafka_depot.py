from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class KafkaDepot(BaseModel):
    brokers: Optional[List[str]]
    schemaRegistryUrl: Optional[str]
    params: Optional[Dict[str, Any]]
