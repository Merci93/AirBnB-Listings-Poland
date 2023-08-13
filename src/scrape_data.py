"""
Scrapes select data from the given URL.
Script specifically written to extract data from AirBnB webpage
"""

import os
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas

from configuration import URL, SAVE_EXTRACTED_DATA, DATA_SOURCE, LOG_DIRECTORY
from logger import log


class ExtractData:
	"""A class to scrape data from given URL."""

	def __init__(self, url: str = None, data_source: str = None, output_directory: str = None) -> None:
		"""
		Open url

		:param url: webpage url
		:param output_directory: location to save scrapped data.
		"""
		self.url = url
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

	def extract_html(self) -> str:
		"""
		Extract data from URL using city name, using headless browser.

		:return: HTML object for each city from the URL.
		"""
		# TODO

	def extract_data(self) -> int:
		"""
		 and extract data from URL.

		:return: Count of data extracted per city.
		"""
		# TODO
		

def scrape_data(url: str = URL,
				data_source: str = DATA_SOURCE,
				output_directory: str = SAVE_EXTRACTED_DATA,
				log_directory: str = LOG_DIRECTORY) -> None:
	"""Scrape data using the provided CSV file containing cities."""
	data_counter = []
	cities = pandas.read_csv(os.path.join(data_source, "cities.csv"))
	for city in cities:
		scraper = ExtractData(url, data_source, output_directory)
		scraper.extract_data()


if __name__ == "__main__":
	scrape_data()



