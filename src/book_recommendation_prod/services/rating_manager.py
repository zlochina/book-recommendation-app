from ..models.schemas import RatingRequest, RatingResponse

class BookRatingManager:
    def add_rating(self, rating: RatingRequest) -> RatingResponse:
        # Placeholder — save to DB here
        return RatingResponse(
            book_id=rating.book_id,
            user_id=rating.user_id,
            rating=rating.rating,
            status="saved"
        )
