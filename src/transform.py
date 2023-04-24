import pandas as pd


def clean_data(csv_file: str) -> pd.DataFrame:
    '''
    Reads in a CSV file of movie data, performs some cleaning operations on it,
    and returns a cleaned DataFrame.

    Args:
        csv_file (str): The name of the CSV file containing the movie data.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    '''
    df = pd.read_csv(csv_file)

    columns = ['id', 'original_title', 'genres', 'popularity', 'release_date',
               'revenue', 'budget', 'title', 'vote_average', 'vote_count']
    df = df[columns]

    df['genres'] = df['genres'].apply(eval)
    df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in x])

    df = df[(df['popularity'] > 0) & (df['revenue'] > 0)
            & (df['budget'] > 0)].reset_index(drop=True)

    return df


def create_kpis_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Given a DataFrame of movie data, creates two new columns representing KPIs
    for each movie: "profitability_success" and "general_popularity".

    The Profitability Success associates the popularity and profitabiity to 
    quantify how comercially successful a given movie is. 
    The General Popularity uses the movie popularity and the count
    of received votes to tell when a movie is popular on both public opinions 
    (votes) and its initial attraction (popularity).

    Args:
        df (pd.DataFrame): The DataFrame of movie data.

    Returns:
        pd.DataFrame: The updated DataFrame with the two new columns.
    '''
    profitability_success = (df['popularity'] * 0.3) + \
        ((df['revenue'] / df['budget']) * 0.7)

    df['profitability_success'] = (profitability_success - profitability_success.min()) / (
        profitability_success.max() - profitability_success.min())

    df['general_popularity'] = (df['popularity'] / df['popularity'].max()
                                * 0.5) + (df['vote_count'] * 0.5 / df['vote_count'].max())
    return df


def transform_data(csv_file: str) -> pd.DataFrame:
    df = clean_data(csv_file)
    df = create_kpis_columns(df)

    return df
