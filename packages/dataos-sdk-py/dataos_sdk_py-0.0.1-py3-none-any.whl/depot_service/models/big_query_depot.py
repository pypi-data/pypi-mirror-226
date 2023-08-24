from typing import Optional, Dict, Any
from pydantic import BaseModel

class BigQueryDepot(BaseModel):
    project: Optional[str]
    params: Optional[Dict[str, Any]]
    temporaryBucket: Optional[str]
    persistentBucket: Optional[str]
