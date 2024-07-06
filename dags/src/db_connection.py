"""Module to create a connection to the PostgreSQL database."""
import psycopg2

from src import config

config.init_settings()


class Connection:
    def db_connect(self) -> psycopg2.connect:
        """Create connection to PostgreSQL database."""
        try:
            connection = psycopg2.connect(dbname=config.settings.staging_db,
                                          user=config.settings.user,
                                          password=config.settings.password,
                                          host=config.settings.host,
                                          port=config.settings.port,
                                          )
            return connection
        except psycopg2.OperationalError:
            raise psycopg2.OperationalError("Unable to connect. Please check parameters")

    def close_connection(self) -> psycopg2:
        """Close active connections to the database."""
        self.db_connect.close()
