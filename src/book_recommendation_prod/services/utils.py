from ..core.book_rec import load_data, preprocess_data
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "csv_data" # TODO: move to config file

def init_pseudo_db():
    print(f"Initialising data...")
    print(f"Loading data...")

    ratings, books = load_data(data_dir=DATA_DIR)
    books['id'] = range(len(books))
    print(f"Preprocessing data...")
    ratings, dataset_preprocessed = preprocess_data(ratings, books)
    print(f"Initialisation finished.")
    return ratings, books, dataset_preprocessed
