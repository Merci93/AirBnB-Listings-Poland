"""Module to load the extracted data into PostgresSQL database."""
from typing import Union

import pandas as pd

from src.db_connection import Connection


class StageData:
    """A class to create a connection the staging database and load data."""
    def __init__(self, data: Union[list, dict]) -> None:
        """Initialize parameters and database connection."""
        self.db_connection = Connection.database_connect(db_name="staging")
        self.data_staged = self.stage_data(data)

    def transform_to_df(self, data: list[dict[str]]) -> pd.DataFrame:
        """Create a Pandas Dataframe from the data."""
        return pd.DataFrame(data)

    def stage_data(self, data: Union[list[dict[str]]]) -> bool:
        """Load data into the staging database."""
        df = self.transform_to_df(data)

        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS data_staging (
                            City VARCHAR(50),
                            Date DATE,
                            Title TEXT,
                            Subtitle TEXT,
                            Bed Type VARCHAR(20),
                            Price per Night INT,
                            Original Price: INT,
                            Availability VARCHAR(20),
                            Total Price INT,
                            Stars INT,
                            Ratings INT,
                        );
                        """)

            insert_data = """INSERT INTO data_staging (
                City, Date, Title, Subtitle, Bed Type, Price per Night, Original Price, Availability, Total Price, Stars, Ratings)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # TODO Update this section for Pandas usage and add additional data points extracted.
            for _, row in df.iterrows():
                cursor.execute(insert_data,
                               row["city"],
                               row["date"],
                               row["title"],
                               row["subtitle"],
                               row["bed_type"],
                               row["price_per_night (zl)"],
                               row["original_price (zl)"],
                               row["availability"],
                               row["total_price (zl)"],
                               row["stars"],
                               row["number_of_ratings"],
                               )

            self.db_connection.commit()
            cursor.close()
            # self.db_connection.close()
            Connection.close_staging_db_connection()

            return True
