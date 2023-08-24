from typing import Optional
from pydantic import BaseModel
from enum import Enum


class GCSDepot(BaseModel):
    bucket: Optional[str]
    relativePath: Optional[str]
    format: Optional[str]
    metastoreUrl: Optional[str]
    icebergCatalogType: Optional[str]

    class IcebergCatalogType(str, Enum):
        HIVE = "HIVE"
        HADOOP = "HADOOP"
