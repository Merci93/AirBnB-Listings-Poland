"""Selenium web driver module"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from log_handler import logger


def init_driver() -> webdriver.Chrome:
    """Instantiate a headless web driver."""
    logger.info("Initializing browser in headless mode ...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-logging")
    options.add_argument("--lang=en-US")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("prefs",
                                    {
                                        "profile.default_content_setting_values.notifications": 2,
                                    }
                                    )
    driver = webdriver.Chrome(options=options)
    logger.info("Driver successfully initialized.")
    return driver
