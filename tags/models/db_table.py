from sqlalchemy import Column, Integer, String

from db_setup import Base


class TagORM(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, index=True)
    movieId = Column(Integer, index=True)
    tag = Column(String, nullable=False)
    timestamp = Column(Integer, default=0, nullable=False)