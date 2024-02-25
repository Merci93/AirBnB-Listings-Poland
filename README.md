# AirBnB Listings in Poland
An analysis of [AirBnB](https://www.airbnb.com) price listing in Poland's major cities. The data used for this analysis was obtained from AirBnB webpage specifically for select cities in Poland which includes but not limited to:
1. Warsaw
2. Wrocław
3. Katowice
4. Gdańsk
5. Łodz
6. Kraków

... for a full list of cities considered in this project, see the **cities.csv** file.

## Objectives
This project was based on finding out and comparing the AirBnB rental listing prices for different accomodations available in these cities for different months of the year. The period will be limited to only one month, but can be extended as required.

## Approach
1. Build a webcrawler to extract data from AirBnB webpage. This script is run on a daily basis, extracting available data from AirBnB webpage.
2. Perform transformations on extracted data and load into PostgreSQL database. In situations where extraction fails, the extracted html data is dumped in a MongoDB database, from where the transformation will be retried.
3. Carry out exploratory and explanatory analysis to understand price differences between house listings in these cities and also explore the price trend.

The project is divided into the following stages:
1. **Data Extraction:** Developed a web scrapping script (using selenium and beaustifulsoup frameworks) to perform the ETL process involving data extraction from the and performing necessary transformations. The output data is loaded into PostgreSQL staging database, and in situations where the transformation fails, the extracted html data is saved as txt file in MongoDb, and the transformation is retried.
2. **Data Cleaning:** Since the first step is focused on data extractions, data cleaning and feature engineering was performed using PySpark.
3. **Exploratory Analysis:** The data was visualized to understand and derive insights from hidden patterns and trends in the data from different cities and in different months.
4. **Power BI Visualization:** Using the cleaned data, a dashboard was created to show the patterns uncovered using appropriate visuals. This visualization will enable travellers and tourists make better financial planning based on the season they are visiting Poland and the city they intend to visit, as they will already have an insight to the average cost of an apartment per night.

The project is containerized using docker, the scrapping orchestration carried out using Apache Airflow. All applications: Airflow, PostgreSQL, and MongoDB are containerized. Docker compose files and directories containing dags 


## Data
The following data were collected from the listings available for each city: 
- Apartment name
- Location/City
- Number of beds
- Price per night
- Rental period
- Total rental price for the rental period
- Rating (star)
- Number of ratings


## Data Modelling
The data model for this project was performed using the **STAR SCHEMA*** in the 3rd normal form (3NF).The model contains one facts table and three dimension tables all linked directly to the facts table. The dimension tables have
a **one to many** and/or **one to one** relationship with the facts table. The tables are as listed below:
1. **Cities**: A dimension table containing the unique cities considered in this project.
2. **Beds**: contains the unique number of beds in the listing, linked to the facts table using their id.
3. **Rental_period**: contains the period (number of days) in which the listing will be available.
4. **Apartments**: A facts table containing the apartment title, subtitles and id's linked to the dimension tables.
This table also contains the price of each listing. These prices includes price per nigh, original price and total
price per listing.

The ERD (Entity Relationship Diagram) was created using the diagramming tool [LucidChart](https://lucid.app/).
![](images/Poland_AirBnB.png)


## Run Instructions
1. Ensure Docker Desktop is installed in the OS, and it is running.
2. Run the `docker_setup.bat` in the command line interface. This file is specifically for Windows OS. This will pull all needed images (Airflow, PostgreSQL, MongoDB) and start the containers.
3. The containers are accessible as follows:
    - Airflow: >>> To be added
    - PostgreSQL PgAdmin: >>> To be added
    - Mongo-expres: >>> To be added default user: admin, default password: pass
4. To stop/close the application, run `docker-compose down --volumes --rmi all`. This will close all containers, pull down all the volumes that has been setup and also removed all pulled docker images.


## Airflow
>>> To be added

## PostgreSQL
>>> To be added

## MongoDB Compass
>>> To be added

## Questions
TODO

## Insights
TODO
