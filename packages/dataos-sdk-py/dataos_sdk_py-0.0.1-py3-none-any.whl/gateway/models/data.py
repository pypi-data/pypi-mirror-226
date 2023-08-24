from pydantic import BaseModel
from pydantic.fields import Optional


class Data(BaseModel,):
    key: Optional[str]
    base64Value: Optional[str]
