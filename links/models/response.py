from typing import Optional
from pydantic import BaseModel

class Link(BaseModel):
    movieId: int
    imdbId: Optional[int] = None
    tmdbId: Optional[int] = None

    model_config = {
        "from_attributes": True
    }
