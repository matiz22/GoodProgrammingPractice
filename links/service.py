from typing import List, Optional

from db_setup import get_session
from links.models.db_table import LinkORM
from links.models.response import Link
from links.models.request import LinkCreate, LinkUpdate


class LinksService:
    """Service layer to fetch links."""

    @staticmethod
    def get_all() -> List[Link]:
        with get_session() as session:
            orm_links = session.query(LinkORM).all()
            return [Link.model_validate({
                "movieId": l.movieId,
                "imdbId": l.imdbId,
                "tmdbId": l.tmdbId
            }) for l in orm_links]

    @staticmethod
    def get_by_id(movie_id: int) -> Optional[Link]:
        with get_session() as session:
            orm_link = session.query(LinkORM).filter(LinkORM.movieId == movie_id).first()
            if not orm_link:
                return None
            return Link.model_validate({
                "movieId": orm_link.movieId,
                "imdbId": orm_link.imdbId,
                "tmdbId": orm_link.tmdbId
            })

    @staticmethod
    def create(link_data: LinkCreate) -> Link:
        with get_session() as session:
            new_link = LinkORM(
                movieId=link_data.movieId,
                imdbId=link_data.imdbId,
                tmdbId=link_data.tmdbId
            )
            session.add(new_link)
            session.commit()
            session.refresh(new_link)
            return Link.model_validate({
                "movieId": new_link.movieId,
                "imdbId": new_link.imdbId,
                "tmdbId": new_link.tmdbId
            })

    @staticmethod
    def update(movie_id: int, link_data: LinkUpdate) -> Optional[Link]:
        with get_session() as session:
            orm_link = session.query(LinkORM).filter(LinkORM.movieId == movie_id).first()
            if not orm_link:
                return None

            if link_data.imdbId is not None:
                orm_link.imdbId = link_data.imdbId
            if link_data.tmdbId is not None:
                orm_link.tmdbId = link_data.tmdbId

            session.commit()
            session.refresh(orm_link)
            return Link.model_validate({
                "movieId": orm_link.movieId,
                "imdbId": orm_link.imdbId,
                "tmdbId": orm_link.tmdbId
            })

    @staticmethod
    def delete(movie_id: int) -> bool:
        with get_session() as session:
            orm_link = session.query(LinkORM).filter(LinkORM.movieId == movie_id).first()
            if not orm_link:
                return False
            session.delete(orm_link)
            session.commit()
            return True
