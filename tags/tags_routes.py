# File: `tags/tags_routes.py`
from typing import List
from fastapi import APIRouter

from tags.tag_model import Tag
from tags.tags_service import TagsService

router = APIRouter(prefix="/tags", tags=["tags"])

# instantiate service (or pass CSV path / call load_from_csv)
tags_service = TagsService("database/tags.csv")

@router.get("/", response_model=List[Tag])
def get_all_tags():
    return list(tags_service.all().values())
