from ..models.schemas import BookRecommendationResponse, BookDetailed, Book
from ..core.book_rec import load_data, preprocess_data, extract_interesting_books, compute_final_rating


class BookManager:
    def __init__(self):
        # TODO: remove this function and move the loading of data onto database
        print(f"Initialising data...")
        print(f"Loading data...")
        ratings, books = load_data()
        print(f"Preprocessing data...")
        self.ratings, self.dataset_preprocessed = preprocess_data(ratings, books)
        print(f"Initialisation finished.")



    def get_recommendations(self, book_id: int) -> BookRecommendationResponse:
        book_title = self._get_book_title_by_id(book_id)
        ratings_data_raw = extract_interesting_books(self.ratings, self.dataset_preprocessed, book_title)
        best_list, _ = compute_final_rating(ratings_data_raw, book_title) # TODO: computing rating should be done when the records are added to the db
        # TODO: create a list of books from ids of best_list
        indices_best = ... #TODO
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
        return self.dataset_preprocessed.iloc[book_id]

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