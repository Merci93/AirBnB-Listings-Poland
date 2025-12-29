@ECHO OFF

REM Check if image already exists
SET IMAGE_NAME=apache/airflow:slim-latest

REM Get image ID if it exists
FOR /F "tokens=*" %%i IN ('docker images -q %IMAGE_NAME%') DO SET IMAGE_EXISTS=%%i

IF NOT DEFINED IMAGE_EXISTS (
    ECHO Image %IMAGE_NAME% not found, building...
    docker build -t %IMAGE_NAME% .
    IF ERRORLEVEL 1 (
        ECHO Failed to build docker image %IMAGE_NAME%.
        EXIT /B 1
    )
    ECHO Image build complete.
) ELSE (
    ECHO Image %IMAGE_NAME% already exists
)

REM Run docker compose
docker-compose up
