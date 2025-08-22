from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    book_id: int
    title: str
    author: str
    image_url_thumb: str

class BookDetailed(Book):
    ISBN: str
    publication_year: int
    publisher: str
    image_url_medium: str
    image_url_large: str
    average_rating: str
    weighted_rating: str
    ratings_count: str


class BookRecommendationResponse(BaseModel):
    book_id: int
    recommendations: List[Book]

class Rating(BaseModel):
    rating_id: int
    user_id: int
    book_isbn: str
    user_rating: int

class RatingsResponse(BaseModel):
    book_id: int
    ratings: List[Rating]
