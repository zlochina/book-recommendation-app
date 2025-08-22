# import
import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import os
import zipfile
import requests

DOWNLOAD_URI = "https://www.kaggle.com/api/v1/datasets/download/arashnic/book-recommendation-dataset"
RATINGS_FNAME = "Ratings.csv"
BOOKS_FNAME = "Books.csv"


### LOADING DATA
def download_kaggle_ds(data_dir):
    # Check if files already exist:
    if all(os.path.exists(os.path.join(data_dir, f)) for f in [BOOKS_FNAME, RATINGS_FNAME]):
        print("Files already exist.")
        return
    url = DOWNLOAD_URI
    dest_path = data_dir / "book-recommendation-dataset.zip"

    os.makedirs(dest_path.parent, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    print(f"Starting download from:\n{url}\n")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    downloaded_size = 0

    with open(dest_path, 'wb') as file:
        for data in response.iter_content(block_size):
            file.write(data)
            downloaded_size += len(data)
            percent = downloaded_size * 100 / total_size if total_size else 0
            print(f"\rDownloaded: {percent:.2f}%", end="")

    print(f"\nDownload complete: {dest_path}")

    print(f"\nExtracting files to:\n{data_dir}\n")
    with zipfile.ZipFile(dest_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        for file in file_list:
            print(f"Extracting: {file}")
        zip_ref.extractall(data_dir)
    print("\nExtraction complete.")

def load_data(download=False, data_dir="csv_data/"):
    data_dir = Path(data_dir)
    # Download from kaggle
    if download:
        download_kaggle_ds(data_dir)
        pass
    # filenames
    # RATINGS_FNAME = "BX-Book-Ratings.csv"
    # BOOKS_FNAME = "BX-Books.csv"

    # read csv files
    print("\n")
    ratings = pd.read_csv(data_dir / RATINGS_FNAME, on_bad_lines="warn")
    print("\n")
    books = pd.read_csv(data_dir / BOOKS_FNAME, on_bad_lines="warn")
    print("\n")
    return (ratings, books)
###

### PREPROCESSING DATA
def preprocess_data(ratings, books):
    # Remove 0 ratings
    ratings = ratings[ratings['Book-Rating'] != 0]

    # Merge Ratings and Books
    dataset = pd.merge(ratings, books, on=['ISBN']) ### INNER JOIN of 2 tables
    # Lowercase all non-numeric columns
    dataset_lowercase=dataset.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)
    return (ratings, dataset_lowercase)
###

def extract_interesting_books(ratings, dataset_lowercase, input_book, ratings_num_th=8):
    assert not ratings is None, f"Ratings should be non None, but {ratings=} was provided"
    assert not dataset_lowercase is None, f"`dataset_lowercase` should be non None, but {dataset_lowercase=} was provided"
    assert input_book, f"`input_book` should be non empty, but {input_book=} was provided"

    ### EXTRACT USER IDS WHO RATED THE INPUT BOOK
    # TODO: do search by regex or other simillar technology. UPD: actually this function should get exact name or id,
    #  and another function should extract the exact name/id by the suggested technique

    user_ids_rated_input_book = dataset_lowercase['User-ID'][
        dataset_lowercase['Book-Title'] == input_book
        ]
    user_ids_rated_input_book = np.unique(user_ids_rated_input_book.tolist())
    ###

    ### EXTRACT DATAROWS WHICH CONTAIN USER ID OF ANY PREVIOUSLY EXTRACTED USER IDS
    # final dataset
    relevant_books = dataset_lowercase[(dataset_lowercase['User-ID'].isin(user_ids_rated_input_book))]
    ###

    ### FILTER DATAROWS (USERS WHICH LEFT MORE THAN th RATINGS) AND EXTRACT "INTERESTING" BOOK TITLES
    # Number of ratings per other books in dataset
    number_of_rating_per_book = relevant_books.groupby(['Book-Title']).agg(
        'count').reset_index()

    # select only books which have actually higher number of ratings than threshold
    books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= ratings_num_th]
    books_to_compare = books_to_compare.tolist()
    ###

    ratings_data_raw = relevant_books[['User-ID', 'Book-Rating', 'Book-Title']][
        relevant_books['Book-Title'].isin(books_to_compare)]

    return ratings_data_raw

def compute_final_rating(ratings_data_raw, input_book):
    ### COMPUTE FINAL RATING
    # TODO: suggest using other rating computation (for example by weighted rating or by number of ratings
    # group by User and Book and compute mean
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()

    # reset index to see User-ID in every row
    ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

    dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
    ###

    ### REMOVE INPUT BOOK FROM DATAFRAME
    # Take out the Lord of the Rings selected book from correlation dataframe
    dataset_of_other_books: pd.DataFrame = dataset_for_corr.copy(deep=False)
    dataset_of_other_books.drop([input_book], axis=1, inplace=True)
    ###

    # empty lists
    book_titles = []
    correlations = []
    avgrating = []

    # corr computation
    for book_title in list(dataset_of_other_books.columns.values):
        book_titles.append(book_title)
        # TODO: maybe add a method to calculate the correlation. Default='pearson'
        # Calculate correlation between (dataframe of input book) and (dataframe without the input book)
        correlations.append(dataset_for_corr[input_book].corr(dataset_of_other_books[book_title]))

        tab = ratings_data_raw[ratings_data_raw['Book-Title'] == book_title].mean(numeric_only=True)

        avgrating.append(tab['Book-Rating'].min())

    # final dataframe of all correlation of each book
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)),
                                   columns=['book', 'corr', 'avg_rating'])

    # top 10 books with highest corr
    sorted_corr_fellowship = corr_fellowship.sort_values('corr', ascending=False)
    best_list = sorted_corr_fellowship.head(10)

    # worst 10 books
    worst_list = sorted_corr_fellowship.tail(10)
    return best_list, worst_list

def main(download, data_dir, book_title, ratings_num_th):
    ratings, books = load_data(download, data_dir)

    ratings, dataset_lowercase = preprocess_data(ratings, books)

    ratings_data_raw = extract_interesting_books(ratings, dataset_lowercase, book_title, ratings_num_th=ratings_num_th)

    best_list, worst_list = compute_final_rating(ratings_data_raw, book_title)

    print(f"Top recommendations: \n{best_list}")
    print(f"Bottom recommendations: \n{worst_list}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--download",
        action="store_true",
        help="Whether to download the csv data into the `data_dir` specified by corresponding argument."
    )
    parser.add_argument("--data_dir",
                        type=str,
                        default="csv_data/",
                        help="Directory for downloading and reading data. Default: \"csv_data/\"")
    parser.add_argument("--ratings_num_th",
                        type=int,
                        default=8,
                        help="Threshold for extracting interesting books, from which recommendations are taken. This number indicates the minimum number of ratings for book to become \"interesting\". Default: 8")
    parser.add_argument(
        "book_title",
        help="Book title to suggest recommendations to.")

    args = parser.parse_args()

    download = args.download if args.download else False
    data_dir = args.data_dir
    book_title = args.book_title
    ratings_num_th = args.ratings_num_th

    main(download, data_dir, book_title, ratings_num_th)