from ..models.schemas import BookRecommendationResponse

class BookManager:
    def get_recommendations(self, user_id: int) -> BookRecommendationResponse:
        # Placeholder — plug in your algorithm here
        return BookRecommendationResponse(
            user_id=user_id,
            recommendations=[
                {"book_id": 1, "title": "Sample Book", "author": "Author A"},
                {"book_id": 2, "title": "Another Book", "author": "Author B"},
            ]
        )
