"""Selenium web driver module"""
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def init_driver(run_headless: bool = True) -> webdriver.Chrome:
    """Instantiate a headless web driver."""

    options = Options()
    if run_headless:
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
    chrome_install = ChromeDriverManager().install()
    install_folder = os.path.dirname(chrome_install)
    service = Service(os.path.join(install_folder, "chromedriver.exe"))
    driver = webdriver.Chrome(service=service, options=options)
    return driver
