@echo off
docker build -t apache/airflow .
docker-compose up
