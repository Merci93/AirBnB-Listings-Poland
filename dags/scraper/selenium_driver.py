"""Selenium web driver module"""
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.log_handler import logger

load_dotenv()

SELENIUM_HOST = os.getenv("SELENIUM_CHROME_CONTAINER_NAME")
SELENIUM_PORT = os.getenv("SELENIUM_CHROME_PORT")


def init_driver(debug: bool = False) -> webdriver.Remote:
    """
    Initialize a safe headless Chrome WebDriver
    """
    chrome_options = Options()

    if not debug:
        logger.info("Initializing headless Chrome driver...")
        chrome_options.add_argument("--headless=new")
    else:
        logger.info("Initializing non-headless Chrome driver...")

    # Required for Docker
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")

    # Interface noise reduction
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--lang=en-US")

    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )
    chrome_options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.notifications": 2,
        },
    )

    driver = webdriver.Remote(
        command_executor=f'http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub',
        options=chrome_options
    )

    driver.set_page_load_timeout(30)

    logger.info("Chrome driver initialized successfully.")

    return driver
