from fastapi import APIRouter, HTTPException, status

from links.models.response import Link
from links.models.request import LinkCreate, LinkUpdate
from links.service import LinksService

router = APIRouter(prefix="/links", tags=["links"])

links_service = LinksService()


@router.get("/", response_model=list[Link])
def get_links():
    """
    Return all links from the database.
    """
    return links_service.get_all()


@router.get("/{movie_id}", response_model=Link)
def get_link(movie_id: int):
    """
    Return a specific link by movieId.
    """
    link = links_service.get_by_id(movie_id)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return link


@router.post("/", response_model=Link, status_code=status.HTTP_201_CREATED)
def create_link(link: LinkCreate):
    """
    Create a new link.
    """
    return links_service.create(link)


@router.put("/{movie_id}", response_model=Link)
def update_link(movie_id: int, link: LinkUpdate):
    """
    Update an existing link.
    """
    updated_link = links_service.update(movie_id, link)
    if not updated_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return updated_link


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(movie_id: int):
    """
    Delete a link by movieId.
    """
    success = links_service.delete(movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
