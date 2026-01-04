"""Selenium web driver module"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from scraper.log_handler import logger


def init_driver(debug: bool = False) -> webdriver.Chrome:
    """
    Initialize a production-safe headless Chrome WebDriver
    """
    chrome_options = Options()

    if not debug:
        logger.info("Initializing headless Chrome driver...")
        chrome_options.add_argument("--headless=new")
    else:
        logger.info("Initializing non-headless Chrome driver...")

    # Required for Docker / CI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # UX / noise reduction
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

    # # Explicit binary paths (critical in Docker)
    chrome_options.binary_location = "/usr/local/bin/google-chrome"

    service = Service("/usr/local/bin/chromedriver")

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options,
    )

    logger.info("Chrome driver initialized successfully.")

    return driver
