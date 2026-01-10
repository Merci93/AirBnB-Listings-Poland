"""Airflow dag parsing test script."""
from airflow.sdk import dag, task
from datetime import datetime, timezone


@dag(
    dag_id="test_minimal_dag",
    schedule=None,
    start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
    catchup=False,
)
def test_dag():

    @task
    def hello():
        return "hello airflow"

    hello()


test_dag()
