from pydantic import BaseModel
from pydantic.fields import Optional


class IcebergPartitionSpecRequest(BaseModel):
    index: int
    type: str
    column: str
    name: Optional[str]
    num_buckets: Optional[int]
