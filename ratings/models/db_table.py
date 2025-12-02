from sqlalchemy import Column, Integer, Float

from db_setup import Base


class RatingORM(Base):
    __tablename__ = "ratings"

    userId = Column(Integer, primary_key=True, index=True)
    movieId = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, default=0, nullable=False)