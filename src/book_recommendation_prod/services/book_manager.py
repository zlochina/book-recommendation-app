from ..models.schemas import BookRecommendationResponse, BookDetailed, Book
from ..core.book_rec import extract_interesting_books, compute_final_rating
from .utils import init_pseudo_db


class BookManager:
    def __init__(self):
        # TODO: remove this function and move the loading of data onto database
        self.ratings, self.books, self.dataset_preprocessed = init_pseudo_db()

    def get_recommendations(self, book_id: int) -> BookRecommendationResponse:
        book_title = self._get_book_title_by_id(book_id).lower()
        ratings_data_raw = extract_interesting_books(self.ratings, self.dataset_preprocessed, book_title)
        best_list, _ = compute_final_rating(ratings_data_raw, book_title) # TODO: computing rating should be done when the records are added to the db
        #
        # thoughts out loud: I thought that what should we do is add additional column of book id for the correlation table,
        # which is create in `compute_final_rating`, but the problem is that there are different published variants of the same book,
        # and ratings are assigned to published variants (ISBN to be exact) rather than the book itself, which means
        # that the rating is calculated based on aggregation of the ratings of every published variant, which MEANS
        # that the original unique ids are irrelevant to the recommendation list.
        # Thus we can edit the correlation calculation function to calculate rating per PUBLISHED VARIANT rather than the book (which semantically gives little sense),
        # or we can choose some book to represent the recommendation (which is implemented below).
        #

        indices_best = list()
        for book_record in best_list['book'].tolist():
            indices_best.append(self._get_book_record_by_title(book_record)["id"])

        recommendations = [Book(
            book_id=book_record["id"],
            title=book_record["Book-Title"],
            author=book_record["Book-Author"],
            image_url_thumb=book_record["Image-URL-S"],
        ) for book_record in [self._get_book_record_by_id(book_id) for book_id in indices_best]]

        return BookRecommendationResponse(
            book_id=book_id,
            recommendations=recommendations,
        )


    def _get_book_record_by_id(self, book_id: int):
        return self.books.iloc[book_id]

    def _get_book_record_by_title(self, book_title: str):
        book_title = book_title.lower()
        variants = self.dataset_preprocessed[self.dataset_preprocessed['Book-Title'] == book_title]["ISBN"]
        return self.books[self.books["ISBN"] == variants.value_counts().idxmax()].iloc[0]

    def _get_book_title_by_id(self, book_id: int) -> str:
        return self._get_book_record_by_id(book_id)["Book-Title"]

    def get_book_details(self, book_id: int) -> BookDetailed:
        book_record = self._get_book_record_by_id(book_id)
        return BookDetailed(
            book_id=book_id,
            title=book_record["Book-Title"],
            author=book_record["Book-Author"],
            ISBN=book_record["ISBN"],
            publication_year=book_record["Year-Of-Publication"],
            publisher=book_record["Publisher"],
            image_url_thumb=book_record["Image-URL-S"],
            image_url_medium=book_record["Image-URL-M"],
            image_url_large=book_record["Image-URL-L"],
            average_rating=None,
            weighted_rating=None,
            ratings_count=None,
        )