from pydantic import BaseModel


class FieldRenameRequest(BaseModel):
    name: str
