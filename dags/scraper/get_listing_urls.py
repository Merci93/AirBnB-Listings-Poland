"""Extract listing urls from airbnb listing page for each city of interest."""
import random
import time
from collections import defaultdict
from typing import Dict, List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from log_handler import logger


class ExtractURL:
    """A class listing url from airbnb webpage."""

    @staticmethod
    def city_url(driver: webdriver, city: str) -> Dict[str, List[str]]:
        """
        A function to extract URL data using the city name.

        :param city: city name
        """
        logger.info(f"Extracting URLs for city {city} ...")

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="search-tabpanel"]/div[1]/div[1]/div[1]/label'))
            )

        except (TimeoutException, ElementNotInteractableException):
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.ffgcxut")))

        try:
            click_path = '//*[@id="search-tabpanel"]/div[1]/div[1]'
            location_search = driver.find_element(By.XPATH, click_path)
            location_search.click()
        except (NoSuchElementException, ElementNotInteractableException):
            location_search = driver.find_element(By.CSS_SELECTOR, "button.ffgcxut")
            location_search.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="search-tabpanel"]/div[1]/div[1]/div[1]/label/div'))
        )

        location_slot = driver.find_element(By.XPATH, '//*[@id="bigsearch-query-location-input"]')
        location_slot.send_keys(Keys.CONTROL, "a")
        time.sleep(random.uniform(2, 3))
        location_slot.send_keys(Keys.DELETE)
        time.sleep(random.uniform(2, 3))
        location_slot.send_keys(city)
        time.sleep(random.uniform(2, 3))
        click_search = driver.find_element(By.CSS_SELECTOR, "button.b1tqc7mb")
        click_search.click()

        city_urls = defaultdict(list)

        while True:
            time.sleep(random.uniform(2, 3))
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.t1jojoys")))
            except TimeoutException:
                pass

            html_body = BeautifulSoup(driver.page_source, "html.parser")
            list_table = html_body.find_all("div", {"class": "c4mnd7m"})
            listing_urls = [f'https://www.airbnb.com/{item.find("a").get("href")}' for item in list_table]
            city_urls[city].extend(listing_urls)

            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.c1ytbx3a")))
                next_page = driver.find_element(By.CSS_SELECTOR, "a.c1ytbx3a")
                next_page.click()
            except (TimeoutException, NoSuchElementException):
                break

        logger.info(f"Listing URL extraction for {city} completed.")
        return {city: city_urls[city]}

    @staticmethod
    def extract_url(driver: webdriver, url: str, cities: List[str]) -> Dict[str, List[str]]:
        """
        Extract listing URLs.

        :param cities: List of cities to extract their listings
        :param url: Webpage url.
        :return: Dictionary containing key-value pairs of city names and a list of listing URLS in the city.
        """
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_1swasop'))).click()
        except (NoSuchElementException, TimeoutException):
            pass

        city_listing_urls = {}
        for city in cities:
            city_listing_urls.update(ExtractURL.city_url(driver=driver, city=f"{city}, Poland"))

        driver.close()
        logger.info("Listing URLs extraction completed, and driver closed.")
        return city_listing_urls
