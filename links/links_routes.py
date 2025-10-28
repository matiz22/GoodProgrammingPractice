from typing import List
from fastapi import APIRouter

from links.link_model import Link
from links.links_service import LinksService

router = APIRouter(prefix="/links", tags=["links"])

links_service = LinksService("database/links.csv")

@router.get("/", response_model=List[Link])
def get_all_links():
    return list(links_service.all().values())
