from fastapi import APIRouter

from links.models.response import Link
from links.service import LinksService

router = APIRouter(prefix="/links", tags=["links"])

links_service = LinksService()


@router.get("/", response_model=list[Link])
def get_links():
    """
    Return all links from the database.
    """
    return LinksService.get_all()
