from typing import Optional
from pydantic import BaseModel
from enum import Enum


class FileDepot(BaseModel):
    path: Optional[str]
    format: Optional[str]
    metastoreUrl: Optional[str]
    icebergCatalogType: Optional[str]

    class IcebergCatalogType(str, Enum):
        HIVE = "HIVE"
        HADOOP = "HADOOP"
