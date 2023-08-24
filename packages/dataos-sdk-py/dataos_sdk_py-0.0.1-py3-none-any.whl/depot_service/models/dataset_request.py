from pydantic.dataclasses import dataclass
from pydantic.fields import Optional, Dict, List, Field


@dataclass
class SchemaRequest:
    type: str = None
    avro: str = None
    mapping: Optional[str] = None


@dataclass
class IcebergPartitionSpecRequest:
    index: int = None
    type: str = None
    column: str = None
    name: str = None


@dataclass
class IcebergRequest:
    specs: Optional[List[IcebergPartitionSpecRequest]] = None
    properties: Optional[Dict[str, str]] = None


@dataclass
class PulsarRequest:
    partitions: int = None
    type: str = None


@dataclass
class DatasetRequest:
    schema_: Optional[SchemaRequest] = Field(alias="schema")
    iceberg: Optional[IcebergRequest] = None
    pulsar: Optional[PulsarRequest] = None
