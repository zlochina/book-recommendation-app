from fastapi import APIRouter, Depends
from ..models.schemas import Book, BookRecommendationResponse, BookDetailed
from ..services.book_manager import BookManager

router = APIRouter()

@router.get("/{book_id}/recommendations", response_model=BookRecommendationResponse)
def get_recommendations(book_id: int, manager: BookManager = Depends()):
    return manager.get_recommendations(book_id)

@router.get("/{book_id}", response_model=BookDetailed)
def get_book_details(book_id: int, manager: BookManager = Depends()):
    return manager.get_book_details(book_id)
