from typing import List, Optional
from db_setup import get_session
from movies.models.db_table import MovieORM
from movies.models.response import Movie


class MoviesService:
    @staticmethod
    def get_all() -> List[Movie]:
        with get_session() as session:
            orm_movies = session.query(MovieORM).all()
            return [Movie.model_validate(m) for m in orm_movies]
