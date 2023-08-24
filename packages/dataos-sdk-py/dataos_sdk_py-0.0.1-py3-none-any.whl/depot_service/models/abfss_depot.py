from enum import Enum
from typing import Optional
from pydantic import BaseModel


class IcebergCatalogType(str, Enum):
    HIVE = "HIVE"
    HADOOP = "HADOOP"


class AbfssDepot(BaseModel):
    account: Optional[str]
    container: Optional[str]
    relativePath: Optional[str]
    format: Optional[str]
    metastoreUrl: Optional[str]
    endpointSuffix: Optional[str]
    icebergCatalogType: Optional[IcebergCatalogType]
