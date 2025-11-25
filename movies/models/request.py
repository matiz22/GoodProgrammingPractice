from pydantic import BaseModel
from typing import Optional


class MovieCreate(BaseModel):
    title: str
    genres: str


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genres: Optional[str] = None

