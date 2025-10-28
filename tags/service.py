from typing import List

from db_setup import get_session
from tags.models.db_table import TagORM
from tags.models.response import Tag


class TagsService:
    """Service to fetch all tags."""

    @staticmethod
    def get_all() -> List[Tag]:
        with get_session() as session:
            orm_tags = session.query(TagORM).all()
            return [
                Tag.model_validate({
                    "userId": t.userId,
                    "movieId": t.movieId,
                    "tag": t.tag,
                    "timestamp": t.timestamp
                }) for t in orm_tags
            ]