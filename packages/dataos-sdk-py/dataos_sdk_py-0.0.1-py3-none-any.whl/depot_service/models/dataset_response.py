from pydantic.fields import Optional, Dict, List, Field
from pydantic import BaseModel


class SchemaResponse(BaseModel):
    type: str
    avro: str
    mapping: Optional[str]


class IcebergPartitionSpecResponse(BaseModel):
    index: int
    type: str
    column: str
    name: str


class IcebergResponse(BaseModel):
    specs: Optional[List[IcebergPartitionSpecResponse]]
    properties: Dict[str, str]
    snapshotId: str
    version: str


class PulsarResponse(BaseModel):
    partitions: int
    type: str


class DatasetResponse(BaseModel):
    schema_: Optional[SchemaResponse] = Field(..., alias='schema')
    iceberg: Optional[IcebergResponse]
    pulsar: Optional[PulsarResponse]
