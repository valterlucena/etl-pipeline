import pandas as pd
from sqlalchemy import create_engine


def load_data(df: pd.DataFrame, db_params: dict) -> None:
    """
    Loads a pandas DataFrame into a PostgreSQL table.

    Args:
        df (pandas.DataFrame): The DataFrame to load.
        db_params (dict): A dictionary containing the database connection parameters.
                          Should have keys 'user', 'password', and 'db'.
    """
    user = db_params['user']
    password = db_params['password']
    db = db_params['db']

    engine = create_engine(
        f"postgresql://{user}:{password}@localhost:5432/{db}")

    df.to_sql('movies', con=engine, if_exists='replace', index=False)
    print("The data was loaded into the database.")
