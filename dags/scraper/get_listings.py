"""Scrapes select data from the given URL, specifically written to extract data from AirBnB webpage."""
import random
import time
from typing import Any, List, Tuple

from bs4 import BeautifulSoup
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.log_handler import logger
from scraper.selenium_driver import init_driver


class ExtractHtml:
    """A class to scrape data from given url."""

    def __init__(self) -> None:
        """Initialize headless browser."""
        self.driver = init_driver()

    def city_html(self, city: str) -> List[Tuple[str, Any]]:
        """
        A function to extract html data using the city name.

        :param city: city name
        """
        logger.info(f"Extracting HTML data for city {city} ...")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="search-tabpanel"]/div[1]/div[1]/div[1]/label'))
            )

        except (TimeoutException, ElementNotInteractableException):
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.ffgcxut")))

        try:
            click_path = '//*[@id="search-tabpanel"]/div[1]/div[1]'
            location_search = self.driver.find_element(By.XPATH, click_path)
            location_search.click()
        except (NoSuchElementException, ElementNotInteractableException):
            location_search = self.driver.find_element(By.CSS_SELECTOR, "button.ffgcxut")
            location_search.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="search-tabpanel"]/div[1]/div[1]/div[1]/label/div'))
        )

        location_slot = self.driver.find_element(By.XPATH, '//*[@id="bigsearch-query-location-input"]')
        location_slot.send_keys(Keys.CONTROL, "a")
        time.sleep(random.uniform(2, 3))
        location_slot.send_keys(Keys.DELETE)
        time.sleep(random.uniform(2, 3))
        location_slot.send_keys(city)
        time.sleep(random.uniform(2, 3))
        click_search = self.driver.find_element(By.CSS_SELECTOR, "button.b1tqc7mb")
        click_search.click()

        city_html = []

        while True:
            time.sleep(random.uniform(2, 3))
            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.t1jojoys")))
            except TimeoutException:
                pass

            html_body = BeautifulSoup(self.driver.page_source, "html.parser")
            city_html.append((city, html_body))

            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.c1ytbx3a")))
                next_page = self.driver.find_element(By.CSS_SELECTOR, "a.c1ytbx3a")
                next_page.click()
            except (TimeoutException, NoSuchElementException):
                try:
                    WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.c1ytbx3a")))
                    next_page = self.driver.find_element(By.CSS_SELECTOR, "a.c1ytbx3a")
                    next_page.click()
                except TimeoutException:
                    break

        logger.info(f"HTML data extraction for {city} completed.")
        return city_html

    def extract_html(self, url: str, cities: List[str]) -> List[Tuple[str, Any]]:
        """
        Extract HTML data from URL using city names.

        :param cities: List of cities to extract their listings
        :param url: Webpage url.
        :return: List containing HTML object for each city from the URL.
        """
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_1swasop'))).click()
        except (NoSuchElementException, TimeoutException):
            pass

        html_list = []
        for city in cities:
            html_list.extend(self.city_html(f"{city}, Poland"))
        # html_list = [item for city in cities for item in self.city_html(f"{city}, Poland")]
        self.driver.close()
        logger.info("HTML data extraction completed, and driver closed.")
        return html_list
