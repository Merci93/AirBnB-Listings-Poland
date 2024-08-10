"""Scrapes select data from the given URL, specifically written to extract data from AirBnB webpage."""
from typing import Any, Dict, List

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.log_handler import logger


class ExtractHtml:
    """A class to scrape data from given url."""

    def __init__(self, url: str) -> None:
        """
        Initialize headless browser.

        :param url: webpage url.
        :param city_file_path: path to csv file containing city names.
        """
        # self.city_file_path = city_file_path

        options = Options()
        options.add_argument('--log-level=3')
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_1swasop'))).click()
        except (NoSuchElementException, TimeoutException):
            pass

    # def read_file(self) -> list:
    #     """
    #     Reads in the csv file containing city names.

    #     :return: A list containing city names.
    #     """
    #     logger.info("Reading city files")
    #     cities = pd.read_csv(self.city_file_path)
    #     city_list = [city['Cities'] for _, city in cities.iterrows()]
    #     logger.info("City file read successfully.")
    #     return city_list

    def extract_html(self, cities: List[str]) -> List[Dict[str, Any]]:
        """
        Extract HTML data from URL using city names.

        :return: list containing HTML object for each city from the URL.
        """
        def city_data(city: str) -> List[str]:
            """
            A helper function to extract html data using the city name.

            :param city: city name
            """
            logger.info(f"Extracting HTML data for city {city} ...")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="search-tabpanel"]/div[1]/div[1]/div[1]/label')))

            except (TimeoutException, ElementNotInteractableException):
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "button.ffgcxut")))

            try:
                click_path = '//*[@id="search-tabpanel"]/div[1]/div[1]'
                location_search = self.driver.find_element(By.XPATH, click_path)
                location_search.click()
            except (NoSuchElementException, ElementNotInteractableException):
                location_search = self.driver.find_element(By.CSS_SELECTOR, "button.ffgcxut")
                location_search.click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="search-tabpanel"]/div[1]/div[1]/div[1]/label/div')
                    )
                )

            location_slot = self.driver.find_element(By.XPATH, '//*[@id="bigsearch-query-location-input"]')
            location_slot.send_keys(Keys.CONTROL, "a")
            location_slot.send_keys(Keys.DELETE)
            location_slot.send_keys(city)
            click_search = self.driver.find_element(By.CSS_SELECTOR, "button.b1tqc7mb")
            click_search.click()

            html_list = []

            while True:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.t1jojoys"))
                        )
                except TimeoutException:
                    pass

                html_body = BeautifulSoup(self.driver.page_source, "html.parser")
                html_list.append((city, html_body))

                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.c1ytbx3a"))
                        )
                    next_page = self.driver.find_element(By.CSS_SELECTOR, "a.c1ytbx3a")
                    next_page.click()
                except (TimeoutException, NoSuchElementException):
                    try:
                        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "a.c1ytbx3a")))
                        next_page = self.driver.find_element(By.CSS_SELECTOR, "a.c1ytbx3a")
                        next_page.click()
                    except TimeoutException:
                        break

            logger.info(f"HTML data extraction for {city} completed.")
            return html_list

        html_list = [city_data(f"{city}, Poland") for city in cities]
        self.driver.close()
        logger.info("HTML data extraction completed, and driver closed.")
        return html_list
