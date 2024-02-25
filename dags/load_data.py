"""A module to load the extracted data into PostgresSQL database."""

import pandas as pd
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
        try:
            self.connection = psycopg2.connect(db_name = data["db_name"],
                                               user = data["user"],
                                               password = data["password"],
                                               host = data["host"],
                                               port = data["port"],
                                               )
        except psycopg2.OperationalError:
            raise "Unable to connect. Please check parameters"
    
    def close_connection(self) -> psycopg2:
        """Close active connections to the database."""
        self.connection.close()

    def transform_to_df(self, data: list[dict[str]]) -> DataFrame:
        """Create a spark Dataframe from the data."""
        return self.spark.createDataFrame(data)

    def load_data(df: DataFrame) -> None:
        """Load data into the database."""
        pass
    
        
    