from fastapi import APIRouter, Depends
from ..models.schemas import RatingsResponse
from ..services.rating_manager import BookRatingManager

router = APIRouter()

@router.get("/{book_id}/ratings", response_model=RatingsResponse)
def get_ratings(book_id: int, manager: BookRatingManager = Depends()):
    return manager.get_ratings(book_id)
