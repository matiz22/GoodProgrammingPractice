from pydantic import BaseModel, Field
from typing import Optional


class RatingCreate(BaseModel):
    userId: int
    movieId: int
    rating: float = Field(..., ge=0.5, le=5.0)
    timestamp: Optional[int] = None


class RatingUpdate(BaseModel):
    rating: float = Field(..., ge=0.5, le=5.0)
    timestamp: Optional[int] = None

