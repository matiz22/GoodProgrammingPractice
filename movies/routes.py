from fastapi import APIRouter, HTTPException, status

from movies.models.response import Movie
from movies.models.request import MovieCreate, MovieUpdate
from movies.service import MoviesService

router = APIRouter(prefix="/movies", tags=["movies"])

movies_service = MoviesService()


@router.get("/", response_model=list[Movie])
def get_movies():
    """
    Return all movies from the database as a list of Movie models.
    """
    return MoviesService.get_all()


@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    """
    Return a single movie by ID.
    """
    movie = MoviesService.get_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    """
    Create a new movie.
    """
    return MoviesService.create(movie.model_dump())


@router.put("/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: MovieUpdate):
    """
    Update an existing movie.
    """
    updated_movie = MoviesService.update(movie_id, movie.model_dump(exclude_none=True))
    if not updated_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return updated_movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    """
    Delete a movie by ID.
    """
    if not MoviesService.delete(movie_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
