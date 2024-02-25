"""A module to load the extracted data into PostgresSQL database."""

import psycopg2
import yaml
from pyspark.sql import DataFrame, SparkSession


class Connection:
    """A class to create a connection the database anc load data."""
    
    def __init__(self, connection_file = "..\connection_file.yml") -> None:
        """Initialize parameters, start spark session and connect to database."""
        self.spark = SparkSession.builder.appName("data transformation").getOrCreate()

        with open(connection_file, "r") as f:
            data = yaml.safe_load(f)
        self.staging_db = data["staging_db"]
        self.main_db = data["main_db"]
        self.user = data["user"]
        self.password = data["password"]
        self.host = data["host"]
        self.port = data["port"]
    
    def close_connection(self) -> psycopg2:
        """Close active connections to the database."""
        self.connection.close()

    def transform_to_df(self, data: list[dict[str]]) -> DataFrame:
        """Create a spark Dataframe from the data."""
        return self.spark.createDataFrame(data)

    def stage_data(self, data: list[dict[str]]) -> None:
        """Load data into the database."""
        df = self.transform_to_df(data)

        try:
            connection = psycopg2.connect(dbname=self.staging_db,
                                          user=self.user,
                                          password=self.password,
                                          host=self.host,
                                          port=self.port,
                                          )
        except psycopg2.OperationalError:
            raise "Unable to connect. Please check parameters"

        cursor = connection.cursor()
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

        # TODO Update this section for spark usage.
        for _, row in df.iterrows():
            cursor.execute(insert_data, row["city"], row["date"], row["title"], row["subtitle"], row["bed_type"],
                           row["price_per_night (zl)"], row["original_price (zl)"], row["availability"],
                           row["total_price (zl)"], row["stars"], row["number_of_ratings"])


        connection.commit()
        cursor.close()
        connection.close()

        return True
    