from typing import Optional
from pydantic import BaseModel


class Wasbs(BaseModel):
    wasbsUrl: Optional[str]
    container: Optional[str]
    account: Optional[str]
    metastoreUrl: Optional[str]
    relativePath: Optional[str]
    icebergCatalogType: Optional[str]
