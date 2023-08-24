from pydantic.fields import Optional, Dict

from pydantic import BaseModel


class AddressInfo(BaseModel):
    depot: Optional[str]
    type: Optional[str]
    collection: Optional[str]
    dataset: Optional[str]
    format: Optional[str]
    external: Optional[bool]
    is_archived: Optional[bool]
    source: Optional[str]
    connection: Optional[Dict]