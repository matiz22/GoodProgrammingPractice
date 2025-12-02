from typing import List
from fastapi import APIRouter, HTTPException, status

from ratings.models.response import Rating
from ratings.models.request import RatingCreate, RatingUpdate
from ratings.service import RatingsService

router = APIRouter(prefix="/ratings", tags=["ratings"])

ratings_service = RatingsService()


@router.get("/", response_model=list[Rating])
def get_ratings():
    """
    Return all ratings from the database.
    """
    return RatingsService.get_all()


@router.get("/{user_id}/{movie_id}", response_model=Rating)
def get_rating(user_id: int, movie_id: int):
    """
    Return a specific rating by userId and movieId.
    """
    rating = RatingsService.get_by_user_and_movie(user_id, movie_id)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    return rating


@router.post("/", response_model=Rating, status_code=status.HTTP_201_CREATED)
def create_rating(rating: RatingCreate):
    """
    Create a new rating.
    """
    return RatingsService.create(rating)


@router.put("/{user_id}/{movie_id}", response_model=Rating)
def update_rating(user_id: int, movie_id: int, rating: RatingUpdate):
    """
    Update an existing rating.
    """
    updated_rating = RatingsService.update(user_id, movie_id, rating)
    if not updated_rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    return updated_rating


@router.delete("/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(user_id: int, movie_id: int):
    """
    Delete a rating by userId and movieId.
    """
    success = RatingsService.delete(user_id, movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
