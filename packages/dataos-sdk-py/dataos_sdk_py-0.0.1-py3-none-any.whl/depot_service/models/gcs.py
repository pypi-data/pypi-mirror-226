from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Gcs(BaseModel):
    gcsUrl: Optional[str]
    bucket: Optional[str]
    path: Optional[str]
    metastoreUrl: Optional[str]
    relativePath: Optional[str]
    icebergCatalogType: Optional[str]

    class IcebergCatalogType(str, Enum):
        HIVE = "HIVE"
        HADOOP = "HADOOP"
