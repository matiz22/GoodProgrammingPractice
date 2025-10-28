from sqlalchemy import Column, Integer

from db_setup import Base


class LinkORM(Base):
    __tablename__ = "links"

    movieId = Column(Integer, primary_key=True, index=True)
    imdbId = Column(Integer, nullable=True)
    tmdbId = Column(Integer, nullable=True)