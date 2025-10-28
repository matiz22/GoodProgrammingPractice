from typing import List
from fastapi import APIRouter

from ratings.models.response import Rating
from ratings.service import RatingsService

router = APIRouter(prefix="/ratings", tags=["ratings"])

ratings_service = RatingsService()


@router.get("/", response_model=list[Rating])
def get_ratings():
    """
    Return all ratings from the database.
    """
    return RatingsService.get_all()

