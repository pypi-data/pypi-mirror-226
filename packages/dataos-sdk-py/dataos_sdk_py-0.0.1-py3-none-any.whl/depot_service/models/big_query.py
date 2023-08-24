from typing import Optional
from pydantic import BaseModel


class Bigquery(BaseModel):
    projectID: Optional[str]
    project: Optional[str]
    dataset: Optional[str]
    table: Optional[str]
