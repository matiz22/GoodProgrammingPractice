from pydantic import BaseModel

class Rating(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int = 0

    model_config = {
        "from_attributes": True
    }