"""Airflow DAG script."""

import os
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from airflow.sdk import dag, task
from airflow.models import Variable


# from dags.log_handler import logger
# from scraper.get_listing_urls import ExtractListingURL
# from scraper.transform_data import ExtractListingData


url = "https://www.airbnb.com/"

DEFAULT_ARGS = {
    "owner": "Airbnb",
    "retries": 2,
    "retry_delay": timedelta(seconds=30),
}


@task
def read_file() -> List[str]:
    """
    Reads the CSV file containing city names.

    :return: List of city names.
    """
    # logger.info("Reading city file")

    file_path = Variable.get(
        "csv_file_path",
        default_var="/opt/airflow/data/cities.csv"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"City file not found: {file_path}")

    cities = pd.read_csv(file_path)

    if "Cities" not in cities.columns:
        raise ValueError("CSV must contain a 'Cities' column")

    city_list = (
        cities["Cities"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    # logger.info("Loaded %d cities", len(city_list))
    return city_list


@dag(
    dag_id="airbnb_read_cities",
    description="Read city list from CSV for data scraping",
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    start_date=datetime(2026, 1, 10),
    catchup=False,
    tags=["airbnb", "etl"],
)
def airbnb_read_cities_dag():
    return read_file()


citties = airbnb_read_cities_dag()


# @task
# def extract_and_transform_listing_data(url: str, cities: List[str]) -> List[Dict[str, Any]]:
#     """Extract listing data from the extracted html for each city."""
#     if url and cities:
#         listing_urls = ExtractURL.extract_url(url=url, cities=cities)
#         # listing_data = ExtractListingData.extract_and_transform_data(html_data=html_data)
#         # return listing_data  # True
#     return False


# def airbnb_pipeline() -> bool:
#     """Execute data extraction and transformation."""
#     listings_html = extract_html(read_file())
#     listings_data = extract_listing_data(listings_html)

#     if listings_data:
#         return True
#     else:
#         return False
