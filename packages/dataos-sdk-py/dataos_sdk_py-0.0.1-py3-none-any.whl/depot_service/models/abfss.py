from enum import Enum
from typing import Optional
from pydantic import BaseModel


class IcebergCatalogType(str, Enum):
    HIVE = "HIVE"
    HADOOP = "HADOOP"


class Abfss(BaseModel):
    wasbsUrl: Optional[str]
    container: Optional[str]
    account: Optional[str]
    metastoreUrl: Optional[str]
    relativePath: Optional[str]
    icebergCatalogType: Optional[IcebergCatalogType]
    abfssUrl: Optional[str]
