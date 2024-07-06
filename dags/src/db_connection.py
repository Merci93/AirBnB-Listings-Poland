"""Module to create a connection to the PostgreSQL database."""
import psycopg2

from src import config

config.init_settings()


class Connection:
    def database_connect(self, db_name: str) -> psycopg2.connect:
        """
        Create connection to PostgreSQL staging database.

        :param: db_name: An indicator of which database to be connected to - staging or main
        """
        database_name = None
        if db_name == "staging":
            database_name = config.settings.staging_db
        elif db_name == "main":
            database_name = config.settings.main_db

        try:
            connection = psycopg2.connect(dbname=database_name,
                                          user=config.settings.user,
                                          password=config.settings.password,
                                          host=config.settings.host,
                                          port=config.settings.port,
                                          )
            return connection
        except psycopg2.OperationalError:
            raise psycopg2.OperationalError("Unable to connect. Please check parameters")

    def close_staging_db_connection(self) -> psycopg2:
        """Close active connections to the staging database."""
        self.database_connect.close()
