from fastapi import APIRouter

from movies.models.response import Movie
from movies.service import MoviesService

router = APIRouter(prefix="/movies", tags=["movies"])

movies_service = MoviesService()


@router.get("/", response_model=list[Movie])
def get_movies():
    """
    Return all movies from the database as a list of Movie models.
    """
    return MoviesService.get_all()
