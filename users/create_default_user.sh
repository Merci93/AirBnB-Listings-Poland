#!/bin/bash

# Script to create a default Airflow user if it doesn't already exist
if ! airflow users list | grep -q '^airbnb\s'; then
  airflow users create \
    --username airbnb \
    --firstname Airbnb \
    --lastname Admin \
    --role Admin \
    --email airbnb@example.com \
    --password airbnb
  echo "Default user created succesfully"
else
  echo "User airbnb already exists, skipping creation."
fi
