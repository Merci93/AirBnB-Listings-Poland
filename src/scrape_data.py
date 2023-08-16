"""
Scrapes select data from the given URL.
Script specifically written to extract data from AirBnB webpage
"""

import os
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas

from configuration import SAVE_EXTRACTED_DATA, DATA_SOURCE, LOG_DIRECTORY, URL, MONTH
from logger import log


class ExtractData:
	"""A class to scrape data from given URL."""

	def __init__(self, url: str = None, month: str = None, data_source: str = None, output_directory: str = None) -> None:
		"""
		Open url

		:param url: webpage url
		:param output_directory: location to save scrapped data.
		"""
		self.url = url
		self.month = month
		self.output_directory = output_directory
		self.data_source = data_source

	def read_file(self) -> list:
		"""
		Read in the csv file containing city names.

		:return: A list containing city names.
		"""
		city_list = []
		cities = pandas.read_csv(os.path.join(self.data_source, "cities.csv"))
		for index, city in cities.iterrows():
			city_list.append(city["Cities"])
		return city_list

	def extract_html(self) -> list:
		"""
		Extract data from URL using city names, and a headless browser.
		
		:return: list containing HTML object for each city from the URL.
		"""
		options = Options()
		options.add_experimental_option("excludeSwitches", ["enable-logging"])
		options.add_argument("--headless")
		driver = webdriver.Chrome(options = options)
		driver.get(self.url)

		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.f19g2zq0")))
		cities = self.read_file()
		html_list = []
		page_per_city = []
		for city in cities:
			city = f"{city}, Poland"
			location_search = driver.find_element(By.CSS_SELECTOR, "button.ffc0w66").click()
			WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.cdhcwpf")))
			location_slot = driver.find_element(By.CSS_SELECTOR, 'input.iluujbk')
			location_slot.send_keys(Keys.CONTROL, "a")
			location_slot.send_keys(Keys.DELETE)
			location_slot.send_keys(city)
			click_search = driver.find_element(By.CSS_SELECTOR, "button.brqqy3t").click()
			
			page = 0
			while True:
				page += 1
				log.info(f"Extracting data from {city} page {page}")
				WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.gsgwcjk")))
				html_body = BeautifulSoup(driver.page_source, "html.parser")
				html_list.append((city, html_body))

				try:
					next_page_path = '//*[@id="site-content"]/div/div[3]/div/div/div/nav/div/a[6]'
					WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.c1ytbx3a")))
					next_page = driver.find_element(By.XPATH, next_page_path).click()
				except NoSuchElementException:
					next_page_path = '//*[@id="site-content"]/div/div[3]/div/div/div/nav/div/a[5]'
					WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.c1ytbx3a")))
					next_page = driver.find_element(By.XPATH, next_page_path).click()
				except TimeoutException:
					break
			
			page_per_city.append([city, page])
		
		return html_list, page_per_city

	def extract_data(self) -> list:
		"""
		 and extract data from URL.

		:return: Count of data extracted per city.
		"""
		# TODO
		pass


def scrape_data(url: str = URL, month: str = MONTH,
				data_source: str = DATA_SOURCE,
				output_directory: str = SAVE_EXTRACTED_DATA,
				log_directory: str = LOG_DIRECTORY) -> None:
	"""Scrape data using the provided CSV file containing cities."""
	cities = pandas.read_csv(os.path.join(data_source, "cities.csv"))
	for city in cities:
		scraper = ExtractData(url, month, data_source, output_directory)
		scraper.extract_html()


if __name__ == "__main__":
	scrape_data()
