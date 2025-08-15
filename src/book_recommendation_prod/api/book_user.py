from fastapi import APIRouter, Depends
from ..models.schemas import Book, BookRecommendationResponse
from ..services.book_manager import BookManager

router = APIRouter()

@router.get("/{user_id}/recommendations", response_model=BookRecommendationResponse)
def get_recommendations(user_id: int, manager: BookManager = Depends()):
    return manager.get_recommendations(user_id)
