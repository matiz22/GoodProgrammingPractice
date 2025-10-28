from typing import List

from pydantic import BaseModel


class Movie(BaseModel):
    movieId: int
    title: str
    genres: List[str]