from sqlalchemy import Column, Integer, JSON, String

from db_setup import Base
from movies.models.response import Movie


class MovieORM(Base):
    __tablename__ = "movies"

    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(JSON, nullable=False)

    def to_pydantic(self) -> Movie:
        return Movie(movieId=self.movieId, title=self.title, genres=self.genres)