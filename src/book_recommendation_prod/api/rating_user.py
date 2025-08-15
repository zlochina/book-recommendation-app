from fastapi import APIRouter, Depends
from ..models.schemas import RatingRequest, RatingResponse
from ..services.rating_manager import BookRatingManager

router = APIRouter()

@router.post("/", response_model=RatingResponse)
def submit_rating(rating: RatingRequest, manager: BookRatingManager = Depends()):
    return manager.add_rating(rating)
