from typing import List

from db_setup import get_session
from links.models.db_table import LinkORM
from links.models.response import Link


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