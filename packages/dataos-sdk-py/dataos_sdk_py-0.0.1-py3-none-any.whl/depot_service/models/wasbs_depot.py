from typing import Optional
from pydantic import BaseModel


class WasbsDepot(BaseModel):
    account: Optional[str]
    container: Optional[str]
    relativePath: Optional[str]
    format: Optional[str]
    metastoreUrl: Optional[str]
    endpointSuffix: Optional[str]
    icebergCatalogType: Optional[str]
