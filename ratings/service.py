from typing import List, Optional

from db_setup import get_session
from ratings.models.db_table import RatingORM
from ratings.models.response import Rating
from ratings.models.request import RatingCreate, RatingUpdate


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

    @staticmethod
    def get_by_user_and_movie(user_id: int, movie_id: int) -> Optional[Rating]:
        with get_session() as session:
            orm_rating = session.query(RatingORM).filter(
                RatingORM.userId == user_id,
                RatingORM.movieId == movie_id
            ).first()
            if not orm_rating:
                return None
            return Rating.model_validate({
                "userId": orm_rating.userId,
                "movieId": orm_rating.movieId,
                "rating": orm_rating.rating,
                "timestamp": orm_rating.timestamp
            })

    @staticmethod
    def create(rating_data: RatingCreate) -> Rating:
        with get_session() as session:
            new_rating = RatingORM(
                userId=rating_data.userId,
                movieId=rating_data.movieId,
                rating=rating_data.rating,
                timestamp=rating_data.timestamp
            )
            session.add(new_rating)
            session.commit()
            session.refresh(new_rating)
            return Rating.model_validate({
                "userId": new_rating.userId,
                "movieId": new_rating.movieId,
                "rating": new_rating.rating,
                "timestamp": new_rating.timestamp
            })

    @staticmethod
    def update(user_id: int, movie_id: int, rating_data: RatingUpdate) -> Optional[Rating]:
        with get_session() as session:
            orm_rating = session.query(RatingORM).filter(
                RatingORM.userId == user_id,
                RatingORM.movieId == movie_id
            ).first()
            if not orm_rating:
                return None

            orm_rating.rating = rating_data.rating
            if rating_data.timestamp is not None:
                orm_rating.timestamp = rating_data.timestamp

            session.commit()
            session.refresh(orm_rating)
            return Rating.model_validate({
                "userId": orm_rating.userId,
                "movieId": orm_rating.movieId,
                "rating": orm_rating.rating,
                "timestamp": orm_rating.timestamp
            })

    @staticmethod
    def delete(user_id: int, movie_id: int) -> bool:
        with get_session() as session:
            orm_rating = session.query(RatingORM).filter(
                RatingORM.userId == user_id,
                RatingORM.movieId == movie_id
            ).first()
            if not orm_rating:
                return False
            session.delete(orm_rating)
            session.commit()
            return True
