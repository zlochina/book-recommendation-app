from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    book_id: int
    title: str
    author: str

class BookRecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[Book]

class RatingRequest(BaseModel):
    user_id: int
    book_id: int
    rating: float

class RatingResponse(BaseModel):
    user_id: int
    book_id: int
    rating: float
    status: str
