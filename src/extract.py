import os
import pandas as pd
import requests

from datetime import datetime
from tqdm import tqdm

API_KEY = '4c5810598f703e8a34f1ab852418770a'
API_URL = 'https://api.themoviedb.org/3'
TOP_RATED = '/movie/top_rated'
MOVIE_DETAILS = 'movie'


def get_movies_ids(num_pages: int = 15) -> list[int]:
    '''
    Retrieves a list of movie IDs for the top rated movies on TMDb.

    Args:
        num_pages (int): The number of pages to retrieve (default is 15).

    Returns:
        list: A list of movie IDs.
    '''
    ids = []
    url_request = f"{API_URL}/{TOP_RATED}"
    session = requests.session()
    with requests.Session() as session:
        for i in range(1, num_pages + 1):
            try:
                params = {'api_key': API_KEY, 'page': i}
                response = session.get(url=url_request, params=params)
                response.raise_for_status()
                top_movies = response.json()
                ids.extend([movie['id'] for movie in top_movies['results']])
            except requests.exceptions.HTTPError as e:
                print(f"An error occurred: {e}")
                break

    return ids


def get_movie_details(movie_id: int) -> dict:
    '''
    Retrieves movie details for a movie ID on TMDb.

    Args:
        movie_id: The Id of the movie.

    Returns:
        A dictionary containing movie details.
    '''
    url_request = f"{API_URL}/{MOVIE_DETAILS}/{movie_id}"
    params = {'api_key': API_KEY}
    with requests.Session() as session:
        try:
            response = session.get(url=url_request, params=params)
            response.raise_for_status()
            movie = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"An error occurred: {e}")
            return {}

    return movie


def get_movies(movie_ids: list[int]) -> list[dict]:
    '''
    Retrieves movie details for a list of movie IDs of TMDb.

    Args:
        ids (list): A list of movie IDs.

    Returns:
        list: A list of dictionaries containing movie details.
    '''
    movies = []
    with tqdm(total=len(movie_ids)) as pbar:
        for i, id in enumerate(movie_ids):
            movie = get_movie_details(id)
            movies.append(movie)
            pbar.update(1)

    return movies


def extract_data() -> str:
    '''
    Retrieve details of top-rated movies from the Movie Database API, stores 
    them in a Pandas Dataframe, and saves the Dataframe in a CSV file.

    Returns:
        str: The name of the created CSV file.
    '''
    ids = get_movies_ids()
    movies = get_movies(ids)
    movies_df = pd.DataFrame(movies)

    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    csv_filename = f"movies_{datetime.now().strftime('%Y-%m-%d')}.csv"
    csv_file = os.path.join(data_dir, csv_filename)
    movies_df.to_csv(csv_file, index=False)

    print(
        f"The extracted data was saved on {os.path.dirname(csv_file)}/ folder.")

    return csv_file
