from pydantic import BaseModel


class SnapshotResponse(BaseModel):
    snapshotId: int
    timestamp: int
