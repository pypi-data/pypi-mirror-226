from typing import Optional
from pydantic import BaseModel


class S3(BaseModel):
    s3Url: Optional[str]
    bucket: Optional[str]
    path: Optional[str]
    metastoreUrl: Optional[str]
    relativePath: Optional[str]
    icebergCatalogType: Optional[str]
