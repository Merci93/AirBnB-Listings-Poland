@ECHO OFF

docker_image_exists() (
    docker images -q %1 2>nul
)

FOR /F "tokens=*" %%i IN ('docker images -q apache/airflow') DO SET IMAGE_EXISTS=%%i

IF NOT DEFINED IMAGE_EXISTS (
    ECHO Image not found, building apache/airflow
    docker build -t apache/airflow:slim-latest .
    ECHO Image build complete.
) ELSE (
    ECHO Image apache/airflow already exists
)

docker-compose up
