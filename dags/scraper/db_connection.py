"""Module to create a connection to the PostgreSQL database."""
import psycopg2

from scraper import config
from scraper.log_handler import logger

config.init_settings()


class Connection:
    """Database connection class."""

    def database_connect(self, db_name: str) -> psycopg2.connect:
        """
        Create connection to PostgreSQL staging database.

        :param: db_name: An indicator of which database to be connected to. Values: "staging" or "main"
        """
        if db_name == "staging":
            logger.info("Connecting to staging database.")
            database_name = config.settings.staging_db
        elif db_name == "main":
            logger.info("Connecting to main database.")
            database_name = config.settings.main_db

        try:
            connection = psycopg2.connect(dbname=database_name,
                                          user=config.settings.user,
                                          password=config.settings.password,
                                          host=config.settings.host,
                                          port=config.settings.port,
                                          )
            logger.info(f"Connection with {database_name} database established.")
            return connection
        except psycopg2.OperationalError:
            raise psycopg2.OperationalError("Unable to connect. Please check parameters")

    def close_staging_db_connection(self) -> psycopg2:
        """Close active connections to the staging database."""
        self.database_connect.close()
        logger.info("Database connection closed.")
