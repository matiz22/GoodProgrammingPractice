from pydantic import BaseModel

class Tag(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int = 0
