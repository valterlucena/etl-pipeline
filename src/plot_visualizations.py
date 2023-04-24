import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine, Engine


def get_most_profitable_movies(engine: Engine) -> pd.DataFrame:
    '''
    Get the most profitable movie for each year since 2010.
    '''

    query = '''
        SELECT DISTINCT ON (YEAR::integer) YEAR::integer, title, profitability_success
        FROM (
            SELECT *, substring(release_date, '\d{4}') AS YEAR
            FROM movies
            WHERE substring(release_date, '\d{4}')::integer >= 2010
        ) AS movies_year
        ORDER BY YEAR::integer, profitability_success DESC;
    '''
    df = pd.read_sql_query(query, engine)

    return df


def plot_most_profitable_movies(engine: Engine, plot_dir: str = "plots") -> None:
    '''
    Create a bar chart showing the most profitable movie for each year since 2010
    and saves it on plots/ directory.
    '''

    df = get_most_profitable_movies(engine)

    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(7, 8))
    sns.barplot(data=df, x='profitability_success', y='year', color='#1f77b4',
                label=df['title'], orient='h')
    for i, (year, success, title) in enumerate(zip(df['year'],
                                                   df['profitability_success'],
                                                   df['title'])):
        if i < len(df['year']) - 1:
            ax.text(success, i, title, ha='left', va='center', fontsize=8)
        else:
            ax.text(success, i, title, ha='right', va='center', fontsize=8)

    ax.set_xlabel('Profitability Success')
    ax.set_ylabel('Year')
    ax.set_title(
        'Movies with Highest Profitability Success per Year (2010-2022)')

    os.makedirs(plot_dir, exist_ok=True)
    fig.savefig(os.path.join(plot_dir, "most_profitable_movies.png"))


def get_average_metrics_by_year(engine: Engine) -> pd.DataFrame:
    '''
    Get the average profitability success and general popularity for each year.
    '''

    query = '''
        SELECT 
            DATE_PART('YEAR', CAST(release_date AS DATE)) AS year,
            AVG(profitability_success) AS avg_profitability_success,
            AVG(general_popularity) AS avg_general_popularity
        FROM movies
        GROUP BY year
        ORDER BY year;
    '''
    df = pd.read_sql_query(query, engine)

    return df


def plot_average_metrics_by_ear(engine: Engine, plot_dir: str = "plots") -> pd.DataFrame:
    '''
    Create a line chart showing the average profitability success and general 
    popularity for each year and saves it on plots/ directory.
    '''

    df = get_average_metrics_by_year(engine)

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(7, 8))
    sns.lineplot(x="year", y="avg_profitability_success",
                 data=df, label="Profitability Success")
    sns.lineplot(x="year", y="avg_general_popularity",
                 data=df, label="General Popularity")
    plt.xlabel("Year")
    plt.ylabel("Average")
    plt.title("Average Profitability Success and General Popularity by Year")
    plt.legend()

    os.makedirs(plot_dir, exist_ok=True)
    fig.savefig(os.path.join(plot_dir, "avg_metrics_by_year.png"))


def plot_visualizations(db_params: dict):
    '''
    Plot the visualizations.
    '''

    user = db_params['user']
    password = db_params['password']
    db = db_params['db']
    engine = create_engine(
        f"postgresql://{user}:{password}@localhost:5432/{db}")

    plot_most_profitable_movies(engine)
    plot_average_metrics_by_ear(engine)

    print("Plots saved on plots/.")
