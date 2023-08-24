from typing import Optional
from pydantic import BaseModel


class S3Depot(BaseModel):
    scheme: Optional[str]
    bucket: Optional[str]
    relativePath: Optional[str]
    format: Optional[str]
    metastoreUrl: Optional[str]
    icebergCatalogType: Optional[str]
