from typing import List, Optional

from db_setup import get_session
from tags.models.db_table import TagORM
from tags.models.response import Tag
from tags.models.request import TagCreate, TagUpdate


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

    @staticmethod
    def get_by_user_and_movie(user_id: int, movie_id: int) -> Optional[Tag]:
        with get_session() as session:
            orm_tag = session.query(TagORM).filter(
                TagORM.userId == user_id,
                TagORM.movieId == movie_id
            ).first()
            if not orm_tag:
                return None
            return Tag.model_validate({
                "userId": orm_tag.userId,
                "movieId": orm_tag.movieId,
                "tag": orm_tag.tag,
                "timestamp": orm_tag.timestamp
            })

    @staticmethod
    def create(tag_data: TagCreate) -> Tag:
        with get_session() as session:
            new_tag = TagORM(
                userId=tag_data.userId,
                movieId=tag_data.movieId,
                tag=tag_data.tag,
                timestamp=tag_data.timestamp
            )
            session.add(new_tag)
            session.commit()
            session.refresh(new_tag)
            return Tag.model_validate({
                "userId": new_tag.userId,
                "movieId": new_tag.movieId,
                "tag": new_tag.tag,
                "timestamp": new_tag.timestamp
            })

    @staticmethod
    def update(user_id: int, movie_id: int, tag_data: TagUpdate) -> Optional[Tag]:
        with get_session() as session:
            orm_tag = session.query(TagORM).filter(
                TagORM.userId == user_id,
                TagORM.movieId == movie_id
            ).first()
            if not orm_tag:
                return None

            orm_tag.tag = tag_data.tag
            if tag_data.timestamp is not None:
                orm_tag.timestamp = tag_data.timestamp

            session.commit()
            session.refresh(orm_tag)
            return Tag.model_validate({
                "userId": orm_tag.userId,
                "movieId": orm_tag.movieId,
                "tag": orm_tag.tag,
                "timestamp": orm_tag.timestamp
            })

    @staticmethod
    def delete(user_id: int, movie_id: int) -> bool:
        with get_session() as session:
            orm_tag = session.query(TagORM).filter(
                TagORM.userId == user_id,
                TagORM.movieId == movie_id
            ).first()
            if not orm_tag:
                return False
            session.delete(orm_tag)
            session.commit()
            return True
