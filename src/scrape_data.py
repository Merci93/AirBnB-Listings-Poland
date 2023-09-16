"""
Scrapes select data from the given URL.
Script specifically written to extract data from AirBnB webpage
"""

import os
import re
import time
import traceback
from datetime import date

import pandas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from unidecode import unidecode

from configuration import SAVE_EXTRACTED_DATA, SAVE_EXTRACTED_DATA_INFO, DATA_SOURCE, LOG_DIRECTORY, URL, MONTH
from logger import log


class ExtractData:
	"""A class to scrape data from given URL."""

	def __init__(self, url: str = None, month: str = None, data_source: str = None, output_directory: str = None,
				 log_directory: str = None, output_data_info: str = None) -> None:
		"""
		Open url

		:param url: webpage url.
		:param output_directory: location to save scrapped data.
		:param month: month when data is extracted.
		:param data_source: path to CSV file containing city names
		:param log_directory: path to where log files are saved.
		:param output_data_info: path to location of CSV file containing city names and number of pages extracted.
		"""
		self.url = url
		self.log_directory  = log_directory
		self.month = month
		self.output_directory = output_directory
		self.data_source = data_source
		self.output_data_info = output_data_info

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
		An output CSV file is generated and saved in the log_directory that contains city names and number of pages
		where data were extracted from each city. File is named <month>_data_extraction.csv, and contains the following
		columns:
		1. City
		2. number_of_pages
		
		:return: list containing HTML object for each city from the URL.
		"""

		def city_data(self, city, driver) -> list:
			"""
			Extract select data using the city name and webdriver.

			:param city: city name
			:param driver: configured chrome webdriver

			:return: lists containing html objects per city, and number of webpages per city.
			"""
			WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.f12fak3r")))
			
			html_list = []
			page_per_city = []
			city = f"{city}, Poland"
			location_search = driver.find_element(By.CSS_SELECTOR, "button.f12fak3r").click()
			WebDriverWait(driver, 10).until(EC.visibility_of_element_located
                                    ((By.XPATH, '//*[@id="search-tabpanel"]/div[1]/div[1]/div[1]/label/div')))
			location_slot = driver.find_element(By.XPATH, '//*[@id="bigsearch-query-location-input"]')
			location_slot.send_keys(Keys.CONTROL, "a")
			location_slot.send_keys(Keys.DELETE)
			location_slot.send_keys(city)
			click_search = driver.find_element(By.CSS_SELECTOR, "button.brqqy3t").click()
			
			page = 0
			while True:
				page += 1
				WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.t1jojoys")))
				log.info(f"Extracting html data from {city} page {page}")
				html_body = BeautifulSoup(driver.page_source, "html.parser")
				html_list.append((city, html_body))

				try:
					WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.c1ytbx3a")))
					next_page = driver.find_element(By.CSS_SELECTOR, "a.c1ytbx3a").click()
				except (TimeoutException, NoSuchElementException):
					try:
						WebDriverWait(driver, 5).until(EC.visibility_of_element_located
                                     ((By.CSS_SELECTOR, "a.c1ytbx3a")))
						next_page = driver.find_element(By.CSS_SELECTOR, "a.c1ytbx3a").click()
					except TimeoutException:
						log.warning(f"Last page reached for {city}.")
						break
			
			page_per_city.append([city, page])
				
			return html_list, page_per_city

		os.makedirs(self.log_directory, exist_ok=True)
		os.makedirs(self.output_data_info, exist_ok=True)

		options = Options()
		options.add_experimental_option("excludeSwitches", ["enable-logging"])
		options.add_argument("--headless")
		driver = webdriver.Chrome(options = options)
		driver.get(self.url)

		cities = self.read_file()
		html_list = []
		page_per_city = []
		for city in cities:
			html_object, pages = city_data(self, city, driver)
			html_list.append(html_object)
			page_per_city.append(pages)

		city_pages = [(item[0], item[1]) for sublist in page_per_city for item in sublist]
		city_pages_df = pandas.DataFrame(city_pages, columns=["city", "number_of_pages"])
		city_pages_df.to_csv(os.path.join(self.output_data_info, f"{date.today()}_data_extraction.csv"), index=False)
		
		return html_list

	def extract_data(self) -> None:
		"""
		Extract listing data from the return HTML object, and save as CSV files.
		
		Output CSV files are saved in the output_directory, in a folder named "month", while "month" is the month when
		the data was extracted. Each file is named after the city which the data belongs to and contains the listing
		details.
		"""
		save_directory = os.path.join(f"{self.output_directory}")
		os.makedirs(save_directory, exist_ok=True)
		
		listing_data = []
		html_list = [(item[0], item[1]) for sublist in self.extract_html() for item in sublist]
		log.info(f"Processing data: tranforming and loading ...")
		for city_html in tqdm(html_list):
			listings = city_html[1].find_all("div", {"class":"c4mnd7m"})
			for list_detail in listings:
				city = city_html[0]
				title = unidecode(list_detail.find("div", {"data-testid":"listing-card-title"}).text)
				subtitle = unidecode(list_detail.find("span", {"data-testid":"listing-card-name"}).text)
				other_details = [item.text for item in list_detail.find_all("span", {"class":"dir dir-ltr"})]
				for item in other_details:
					if ("bed" in item) or ("beds" in item):
						bed_type = item 
					if "–" in item:
						availability = item.replace("–", "-")
				try:
					stars = list_detail.find("span", {"class":"r1dxllyb"}).text.split("(")[0].strip()
				except AttributeError as e:
					stars = e
				try:
					no_of_ratings = list_detail.find("span",
													 {"class":"r1dxllyb"}
													).text.split("(")[1].strip().replace(")","")
				except (IndexError, AttributeError):
					no_of_ratings = stars
				total_price = list_detail.find("div", {"class":"_tt122m"}).text.split("zł")[0].strip()
				get_price = list_detail.find("span", {"class":"_14y1gc"}).text
				if "originally" in str(get_price):
					price_per_night = get_price.split("zł")[1].strip()
					original_price = get_price.split("zł")[0].strip()
				else:
					price_per_night = get_price.split("zł")[0].strip()
					original_price = price_per_night

				listing_data.append({"city": city,
									 "date": date.today(),
									 "title": title,
									 "subtitle": subtitle,
									 "bed_type": bed_type,
									 "price_per_night (zl)": price_per_night,
									 "original_price (zl)": original_price,
									 "total_price (zl)": total_price,
									 "availability": availability,
									 "star": stars,
									 "number_of_ratings": no_of_ratings
									 })
		city_listings_df = pandas.DataFrame(listing_data, columns=["city", "date", "title", "subtitle",
																   "price_per_night (zl)", "original_price (zl)",
																   "availability", "total_price (zl)", "bed_type",
																   "star", "number_of_ratings",
																  ])
		city_listings_df.to_csv(os.path.join(save_directory, f"{date.today()}_data.csv"), index=False)
		log.info(f"Files for {date.today()} saved.")


def scrape_data(url: str = URL, month: str = MONTH,
				data_source: str = DATA_SOURCE,
				output_directory: str = SAVE_EXTRACTED_DATA,
				log_directory: str = LOG_DIRECTORY,
				output_data_info: str = SAVE_EXTRACTED_DATA_INFO) -> None:
	"""Scrape data using the provided CSV file containing cities."""
	
	scraper = ExtractData(url, month, data_source, output_directory, log_directory, output_data_info)
	try:
		scraper.extract_data()
	except (TimeoutException, NoSuchElementException) as e:
		traceback_string = traceback.format_exc()
		traceback_string = traceback_string.split("Message")[0]
		log.warning(f"An exceptionoccured. \nCheck log for description. Terminating program. \n\n{traceback_string}")


if __name__ == "__main__":
	scrape_data()
