from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define default_args dictionary to specify the DAG's default parameters
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'hello_airflow_dag',
    default_args=default_args,
    description='A simple DAG to print "Hello, Airflow!"',
    schedule_interval=timedelta(days=1),  # Set the schedule interval to daily
)

# Define a Python function that will be executed by the task
def print_hello():
    print("Hello, Airflow!")

# Create a PythonOperator task that will run the print_hello function
hello_task = PythonOperator(
    task_id='print_hello_task',
    python_callable=print_hello,
    dag=dag,
)

# Set the task dependencies (in this case, no dependencies)
hello_task

if __name__ == "__main__":
    dag.cli()
