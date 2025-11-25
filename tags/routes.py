# File: `tags/tags_routes.py`
from typing import List
from fastapi import APIRouter, HTTPException, status

from tags.models.response import Tag
from tags.models.request import TagCreate, TagUpdate
from tags.service import TagsService

router = APIRouter(prefix="/tags", tags=["tags"])

tags_service = TagsService()

@router.get("/", response_model=List[Tag])
def get_tags():
    """
    Return all tags from the database.
    """
    return TagsService.get_all()

@router.get("/{user_id}/{movie_id}", response_model=Tag)
def get_tag(user_id: int, movie_id: int):
    """
    Return a specific tag by userId and movieId.
    """
    tag = TagsService.get_by_user_and_movie(user_id, movie_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag

@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate):
    """
    Create a new tag.
    """
    return TagsService.create(tag)

@router.put("/{user_id}/{movie_id}", response_model=Tag)
def update_tag(user_id: int, movie_id: int, tag: TagUpdate):
    """
    Update an existing tag.
    """
    updated_tag = TagsService.update(user_id, movie_id, tag)
    if not updated_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return updated_tag

@router.delete("/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(user_id: int, movie_id: int):
    """
    Delete a tag by userId and movieId.
    """
    success = TagsService.delete(user_id, movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
