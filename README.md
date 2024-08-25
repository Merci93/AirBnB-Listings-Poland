# AirBnB Listings in Poland
A data engineering project using [AirBnB](https://www.airbnb.com) listings in select cities Poland. The data used for this analysis was obtained from AirBnB webpage specifically for the following cities:
1. Warsaw
2. Wrocław
3. Katowice
4. Gdańsk
5. Łodz
6. Kraków
7. Lublin
8. Poznan
9. Zakopane
10. Gliwice
11. Torun
12. Biesko-Biała
13. Gdynia
14. Sosnowiec


## Objectives
This project is aimed at building an ETL pipeline that includes the following:
1. Data collection - webscraping data from airbnb webpage page, specifically for listings in Poland.
2. Cleaning and transformation - extracting useful data from the html, and transforming into a Spark dataframe.
3. Loading into PostgreSQL database via robust FastAPI endpoints.
4. Orchestrating with Apache Airflow.
5. Containerization using Docker.


## Approach
1. Build a webcrawler to extract data from AirBnB webpage using Selenium and BeautifulSoup to collect data for select cities in Poland.
2. Perform transformations on extracted data and load into PostgreSQL database.
3. Orchestrating process using Apache Airflow and containerizing using Docker.
4. Perform exploratory and explanatory analysis to understand price differences between house listings in these cities and also explore the price trend, listing details, ammenities, etc.

The project is divided into the following stages:
1. **Data Extraction:** Developed a web scrapping script (using Selenium and Beaustifulsoup frameworks) to perform the ETL process involving data extraction from the and performing necessary transformations. The output data is loaded into PostgreSQL staging database.
2. **Data Cleaning:** Since the first step is focused on data extractions, data cleaning and feature engineering will be performed.
3. **Exploratory Analysis:** The data will be visualized to understand and derive insights from hidden patterns and trends in the data from different cities and in different months.
4. **Power BI Visualization:** Using the cleaned data, a dashboard will be created to show the patterns uncovered using appropriate visuals. This visualization will enable travellers and tourists make better financial planning based on the season they are visiting Poland and the city they intend to visit, as they will already have an insight to the average cost of an apartment per night.

The project is containerized using Docker, the scrapping orchestration carried out using Apache Airflow. All applications: Airflow and PostgreSQL are containerized using Docker, and interaction with the PostgreSQL database powered by a robust FastAPI backend.


## Data
The following data were collected from the listings available for each city:
- Apartment Id
- Apartment name/title
- Location/City
- Number of beds
- Price per night
- Rental period
- Guests
- Bedrooms
- Bath
- check in date
- check out date
- Ammenities - (as presence of bathtub, kitchen, iron, oven, electric kettle, heating, etc)
- Star
- Number of ratings
- Review ratings (Cleanliness, Accuracy, Check in, Communication, Location, Value)
- Top 3 reviews


## Data Modelling
The data model for this project was performed using the **SNOWFLAKE SCHEMA*** in the 3rd normal form (3NF).The model contains one facts table and three dimension tables all linked directly to the facts table. The dimension tables have a **one to many** and/or **one to one** relationship with the facts table. The tables are as listed below:
1. **City**: A dimension table containing the unique cities considered in this project.
2. **Ratings**: contains the ratings per listing.
3. **Rental_period**: contains the period (number of days) the listing will be available - check in and check out date.
4. **Apartments**: A facts table containing the apartment title, subtitles and id's linked to the dimension tables.
This table also contains the price of each listing. These prices includes price per nigh, original price and total
price per listing.
5. **Details**: further details relating to the listing: beds, bath, quests and bedroom.
6. **Reviews**: Reviews for the listing, with an extende table, **country** which keeps unique reviewer's country.

The ERD (Entity Relationship Diagram) was created using the diagramming tool [LucidChart](https://lucid.app/).
![](img/Poland_AirBnB.png)


## Run Instructions
1. Ensure Docker Desktop is installed in the OS, and it is running.
2. Run the `docker_setup.bat` in the command line interface. This file is specifically for Windows OS. This will pull all needed images (Airflow, PostgreSQL, MongoDB) and start the containers.
3. The containers are accessible as follows:
    - Airflow: >>> To be added
    - PostgreSQL: >>> To be added
    - API Endpoints >>> To be added
4. To stop/close the application, run `docker-compose down --volumes --rmi all`. This will close all containers, pull down all the volumes that has been setup and also removed all pulled docker images.


## Airflow
>>> To be added

## API Endpoints
>>> To be added

## Questions
TODO

## Insights
TODO
