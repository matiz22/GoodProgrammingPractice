# python
from typing import List
from fastapi import APIRouter

from ratings.rating_model import Rating
from ratings.ratings_service import RatingsService

router = APIRouter(prefix="/ratings", tags=["ratings"])

# instantiate service (or pass CSV path to constructor / call load_from_csv)
ratings_service = RatingsService("database/ratings.csv")

@router.get("/", response_model=List[Rating])
def get_all_ratings():
    return list(ratings_service.all().values())
