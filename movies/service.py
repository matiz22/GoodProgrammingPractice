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

    @staticmethod
    def get_by_id(movie_id: int) -> Optional[Movie]:
        with get_session() as session:
            orm_movie = session.query(MovieORM).filter(MovieORM.movieId == movie_id).first()
            return Movie.model_validate(orm_movie) if orm_movie else None

    @staticmethod
    def create(movie_data: dict) -> Movie:
        with get_session() as session:
            orm_movie = MovieORM(**movie_data)
            session.add(orm_movie)
            session.commit()
            session.refresh(orm_movie)
            return Movie.model_validate(orm_movie)

    @staticmethod
    def update(movie_id: int, movie_data: dict) -> Optional[Movie]:
        with get_session() as session:
            orm_movie = session.query(MovieORM).filter(MovieORM.movieId == movie_id).first()
            if not orm_movie:
                return None
            for key, value in movie_data.items():
                if value is not None:
                    setattr(orm_movie, key, value)
            session.commit()
            session.refresh(orm_movie)
            return Movie.model_validate(orm_movie)

    @staticmethod
    def delete(movie_id: int) -> bool:
        with get_session() as session:
            orm_movie = session.query(MovieORM).filter(MovieORM.movieId == movie_id).first()
            if not orm_movie:
                return False
            session.delete(orm_movie)
            session.commit()
            return True
