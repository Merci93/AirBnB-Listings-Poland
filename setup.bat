@echo off
docker build -t apache/airflow:slim-latest .
docker-compose up
