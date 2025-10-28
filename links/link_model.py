from pydantic import BaseModel

class Link(BaseModel):
    movieId: int
    imdbId: str = ""
    tmdbId: str = ""
