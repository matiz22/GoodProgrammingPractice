# File: `tags/tags_routes.py`
from typing import List
from fastapi import APIRouter

from tags.models.response import Tag
from tags.service import TagsService

router = APIRouter(prefix="/tags", tags=["tags"])

tags_service = TagsService()

@router.get("/", response_model=List[Tag])
def get_tags():
    """
    Return all tags from the database.
    """
    return TagsService.get_all()
