# python
from typing import List, Dict, Any
from fastapi import APIRouter

from movies.movies_service import MoviesService

router = APIRouter(prefix="/movies", tags=["movies"])

movies_service = MoviesService("database/movies.csv")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_movies():
    """
    Return all movies as a list of dicts.
    """
    return list(movies_service.all().values())
