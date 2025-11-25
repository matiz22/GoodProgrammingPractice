from pydantic import BaseModel
from typing import Optional


class TagCreate(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: Optional[int] = None


class TagUpdate(BaseModel):
    tag: str
    timestamp: Optional[int] = None

