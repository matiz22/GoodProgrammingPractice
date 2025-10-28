from typing import List

from db_setup import get_session
from ratings.models.db_table import RatingORM
from ratings.models.response import Rating


class RatingsService:
    """Service to fetch all ratings."""

    @staticmethod
    def get_all() -> List[Rating]:
        with get_session() as session:
            orm_ratings = session.query(RatingORM).all()
            return [Rating.model_validate({
                "userId": r.userId,
                "movieId": r.movieId,
                "rating": r.rating,
                "timestamp": r.timestamp
            }) for r in orm_ratings]