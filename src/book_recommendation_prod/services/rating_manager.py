from ..models.schemas import RatingsResponse, Rating
from .utils import init_pseudo_db

class BookRatingManager:
    def __init__(self):
        _, self.books, self.dataset_preprocessed = init_pseudo_db()
        self.dataset_preprocessed["rating-id"] = range(len(self.dataset_preprocessed))

    def get_ratings(self, book_id) -> RatingsResponse:
        ratings = list()
        book_title = self.books.iloc[book_id]['Book-Title'].lower()
        records = self.dataset_preprocessed[self.dataset_preprocessed['Book-Title'] == book_title]
        for _, record in records.iterrows():
            ratings.append(Rating(
                rating_id=int(record['rating-id']),
                user_id=record['User-ID'],
                book_isbn=record["ISBN"],
                user_rating=record["Book-Rating"],
            ))

        return RatingsResponse(
            book_id=book_id,
            ratings=ratings
        )
