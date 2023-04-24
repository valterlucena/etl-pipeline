from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data
from src.plot_visualizations import plot_visualizations


def main():
    print("Extracting data...")
    csv_file = extract_data()

    print("Cleaning the extracted data and creating KPIs...")
    df = transform_data(csv_file)

    print("Loading the transformed data into the Database...")
    db_params = {
        'user': 'postgres',
        'password': 'postgres',
        'db': 'moviesdb'
    }
    load_data(df, db_params)

    print("Creating plots for KPIs...")
    plot_visualizations(db_params)

if __name__ == "__main__":
    main()