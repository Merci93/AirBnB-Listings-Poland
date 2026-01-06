"""Extract listing urls from airbnb listing page for each city of interest."""
from typing import Dict, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.log_handler import logger
from scraper.selenium_driver import init_driver


class ExtractListingURL:
    """A class to handle listing URL extraction from the webpage."""
    def __init__(self, base_url: str, cities: list[str], max_pages: int, debug: bool) -> None:
        """
        Initialize the ExtractListingURL class.

        :param url: Base webpage URL.
        :param cities: List of cities to extract listings for.
        :param max_pages: Maximum number of pages to scrape.
        :param debug: Enable debug mode.
        """
        self.debug = debug
        self.max_pages = max_pages
        self.base_url = base_url
        self.cities = cities if isinstance(cities, list) else [cities]

    def extract_url(self) -> Dict[str, List[str]]:
        """
        Extract listing URLs per city.

        :return: Dict mapping city name -> list of listing URLs.
        """
        logger.info("Starting listing URL extraction")
        results: Dict[str, List[str]] = {}

        for city in self.cities:
            driver = None
            try:
                logger.info("Processing city: %s", city)

                driver = init_driver(debug=self.debug)

                logger.info("Wait while data is being extracted and processed for city %s...", city)

                results[city] = self._extract_city(driver, city)

            except Exception as exc:
                logger.exception("Failed for city %s: %s", city, exc)
                results[city] = []

            finally:
                if driver:
                    driver.quit()

        logger.info("Listing URL extraction completed")
        return results

    def _extract_city(self, driver: WebDriver, city: str) -> List[str]:
        """
        Extract listing URLs for a specific city.

        :param driver: Selenium WebDriver instance
        :param city: City name to search for
        :return: List containing listing URLs for the city
        """
        driver.get(self.base_url)

        self._dismiss_popups(driver)
        self._search_city(driver, f"{city}, Poland")

        collected: set[str] = set()
        page_count = 0

        while page_count < self.max_pages:
            page_count += 1
            self._wait_for_listings(driver)

            urls = self._extract_listing_urls_from_page(driver)
            if not urls:
                break  # no listings found, stop

            before = len(collected)
            collected.update(urls)

            if len(collected) == before:
                break  # no new data, stop

            if not self._next_page(driver):
                break  # no next page, stop

        return list(collected)

    def _dismiss_popups(self, driver: WebDriver) -> None:
        """
        Dismiss any pop-ups or modals that may interfere with scraping.

        :param driver: Selenium WebDriver instance
        """
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "fp9kp52"))).click()
        except (TimeoutException, NoSuchElementException):
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))).click()
        except Exception:
            pass

    def _search_city(self, driver: WebDriver, city: str) -> None:
        """
        Search for a city using the Airbnb search functionality.

        :param driver: Selenium WebDriver instance
        :param city: City name to search for
        """
        search = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "bigsearch-query-location-input"))
        )
        search.clear()
        search.send_keys(city)
        search.send_keys(Keys.ENTER)
        click_search = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Search']")
        click_search.click()

    def _wait_for_listings(self, driver: WebDriver) -> None:
        """
        Wait for the listing elements to load on the page.

        :param driver: Selenium WebDriver instance
        """
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/rooms/']"))
            )
        except TimeoutException:
            # In headless mode, sometimes elements take longer to load or cannot be found
            # but these elements are already there, skip and continue
            pass

    def _extract_listing_urls_from_page(self, driver: WebDriver) -> List[str]:
        """
        Extract listing URLs from the current page.

        :param driver: Selenium WebDriver instance
        :return: List of listing URLs
        """
        anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='/rooms/']")
        return [href for a in anchors if (href := a.get_attribute('href'))]

    def _next_page(self, driver: WebDriver) -> bool:
        """
        Navigate to the next page of listings if available.

        :param driver: Selenium WebDriver instance
        :return: True if navigated to next page, False otherwise
        """
        try:
            next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
            next_button.click()
            return True
        except (TimeoutException, NoSuchElementException):
            logger.info("No more pages available.")
            return False
