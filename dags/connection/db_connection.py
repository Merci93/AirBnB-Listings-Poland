"""Module to create a connection to the PostgreSQL database."""
import psycopg2
from psycopg2.extensions import connection

from dags.config.config import settings
from dags.utils.log_handler import logger


class DatabaseConnector:
    """PostgreSQL database connection factory."""

    def database_connect(self, db_name: str) -> connection:
        if db_name == "staging":
            logger.info("Connecting to staging database.")
            database_name = settings.staging_db
        elif db_name == "main":
            logger.info("Connecting to main database.")
            database_name = settings.main_db
        else:
            raise ValueError("db_name must be either 'staging' or 'main'")

        try:
            conn = psycopg2.connect(
                dbname=database_name,
                user=settings.user,
                password=settings.password,
                host=settings.host,
                port=settings.port,
            )
            logger.info(f"Connection with {database_name} database established.")
            return conn
        except psycopg2.OperationalError:
            logger.exception("Unable to connect to database")
            raise

    @staticmethod
    def close_db_connection(conn: connection) -> None:
        if conn and not conn.closed:
            conn.close()
            logger.info("Database connection closed.")
