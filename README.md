To run the pipeline, follow the steps bellow:

1. Start the Postgres service running the following command in the terminal.

```zsh
docker compose up --build -d
```

2. Create and activate a Python virtual environment:

```zsh
python -m venv env
source env/bin/activate
```

3. Install the necessary dependencies

```zsh
pip install -r requirements.txt
```

4. Once the dependencies are installed and the database service is up and running, execute the following command to run the entire ETL pipeline:

```zsh
python etl.py
```

This command will run a ETL pipeline that extracts data from the [TMDb Movie API](https://developers.themoviedb.org/4/getting-started), transforms it into a desired format and creates two KPIs, loads it into a Postgres database and generate visualizations using the created KPIs.

## KPIs

### **Profitability Success**

Associates the popularity and profitabiity to quantify how comercially successful a given movie is and it's calculated as:

```python
profitability_success = (popularity * 0.3) + ((revenue / budget) * 0.7)
```

The popularity and revenue-to-budget ratio are weighted differently, with the revenue-to-budget ratio being more heavily weighted so that profitability has more impact in measuring the commercial success of a movie. The result is then scaled using the MinMax scale so all its values lies between 0 and 1.

### **General Popularity**

Uses the movie popularity and the count of received votes to tell when a movie is popular on both public opinions (votes) and its initial attraction (popularity). It's calculated as:

```python
general_popularity = (popularity / max(popularity) * 0.5) + (vote_count * 0.5 / max(vote_count))
```

The popularity and vote count are normalized to their respective maximum values and then weighted equally so both factors have the same impact in measuring the general popularity of a movie.
