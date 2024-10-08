"""Scrapes select data from the given URL, specifically written to extract data from AirBnB webpage."""
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unidecode import unidecode

from scraper.log_handler import logger
from scraper.selenium_driver import init_driver


class ExtractListingData:
    """
    A class to get listing HTML data from the listing URL, and extract required listing data and return
    a dictionary of extracted informations.
    """

    @staticmethod
    def extract_and_transform_data(city: str, listing_url: str) -> List[Dict[str, Any]]:
        """
        Extract listing data from the listing url, and return list of dictionaries with extracted data.

        :param city: City name.
        :param listing_url: Listing URL string.
        """
        driver = init_driver()
        wait = WebDriverWait(driver, 10)

        driver.get(listing_url)
        try:
            time.sleep(random.uniform(2, 3))
            driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()
        except Exception:
            pass

        time.sleep(random.uniform(2, 3))
        listing_html = BeautifulSoup(driver.page_source, "html.parser")

        listing_id = listing_url.split("?")[0].rsplit("/", 1)[-1]
        listing_title = unidecode(listing_html.title.text)
        specs = [re.sub("·", "", item.text).strip() for item in listing_html.find_all("li", {"class": "l7n4lsf"})]
        guests = next((item for item in specs if "guest" in item), "N/A")
        bathroom = next((item for item in specs if "bath" in item), "N/A")
        bedroom = next((item for item in specs if re.search(r"\bbed(s)?\b", item)), "N/A")
        apartment_type = next((item for item in specs if "studio" in item.lower() or "bedroom" in item.lower()), "N/A")
        try:
            price_per_night = unidecode(listing_html.find("span", {"class": "_11jcbg2"}).text)
        except Exception:
            price_per_night = "N/A"
        try:
            stars = float(listing_html.find("div", {"class": "r1lutz1s"}).text)
        except Exception:
            try:
                stars = float(re.search(r"\d.{3}", listing_html.find("a", {"class": "l1ovpqvx"}).text, re.IGNORECASE).group())
            except Exception:
                stars = "N/A"

        try:
            no_of_reviews = re.sub(
                "Reviews", " reviews", re.search(r'\d+\s*Reviews?', listing_html.find("a", {"class": "l1ovpqvx"}).text).group(),
                re.IGNORECASE
            )
        except Exception:
            try:
                no_of_reviews = listing_html.find("a", {"class": "l1ovpqvx"}).text
            except Exception:
                no_of_reviews = "N/A"

        try:
            check_in_date = datetime.strptime(
                listing_html.find("div", {"class": "_19y8o0j"}).find("div", {"class": "_tekaj0"}).text.strip(), "%m/%d/%Y"
            ).date()
        except Exception:
            check_in_date = "Missed"

        try:
            check_out_date = datetime.strptime(
                listing_html.find("div", {"class": "_48vms8s"}).find("div", {"class": "_tekaj0"}).text.strip(), "%m/%d/%Y"
            ).date()
        except Exception:
            check_out_date = "Missed"

        overall_rating = [item.text for item in listing_html.find_all("div", {"class": "c18arpj7"})]
        cleanliness = next((float(re.search(r"\d.{2}", item).group()) for item in overall_rating if "cleanliness" in item), "N/A")
        accuracy = next((float(re.search(r"\d.{2}", item).group()) for item in overall_rating if "accuracy" in item), "N/A")
        check_in = next((float(re.search(r"\d.{2}", item).group()) for item in overall_rating if "check-in" in item), "N/A")
        comm = next((float(re.search(r"\d.{2}", item).group()) for item in overall_rating if "communication" in item), "N/A")
        location = next((float(re.search(r"\d.{2}", item).group()) for item in overall_rating if "location" in item), "N/A")
        value = next((float(re.search(r"\d.{2}", item).group()) for item in overall_rating if "value" in item), "N/A")
        try:
            host_response_rate = re.search(r'\b\d{1,3}%\b', listing_html.find("div", {"class": "h1geptgj"}).text).group()
        except Exception:
            host_response_rate = "N/A"

        click_action = ActionChains(driver)
        xpath = "//button[starts-with(text(), 'Show all') and (contains(text(), 'amenities') or contains(text(), 'amenity details'))]"
        show_ammenities = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        click_action.move_to_element(show_ammenities).click().perform()
        time.sleep(random.uniform(2, 3))
        ammenities_html = BeautifulSoup(driver.page_source, "html.parser")
        ammenities = [
            item.text.lower()
            for item in ammenities_html.find_all("div", {"class": "_3hmsj"})[-1].find_all("div", {"class": "rten07p"})
            if "Unavailable" not in item.text
        ]
        bathtub = next(("Yes" for item in ammenities if "bathtub" in item), "No")
        hot_water = next(("Yes" for item in ammenities if "hot water" in item), "No")
        hangers = next(("Yes" for item in ammenities if "hanger" in item), "No")
        bed_linens = next(("Yes" for item in ammenities if "bed linen" in item), "No")
        iron = next(("Yes" for item in ammenities if "iron" in item), "No")
        kitchen = next(("Yes" for item in ammenities if "kitchen" in item), "No")
        wifi = next(("Yes" for item in ammenities if "wifi" in item), "No")
        elevator = next(("Yes" for item in ammenities if "wifi" in item), "No")
        washer = next(("Yes" for item in ammenities if "washer" in item), "No")
        parking = next(("Yes" for item in ammenities if "parking" in item or "garage" in item), "No")
        workspace = next(("Yes" for item in ammenities if "workspace" in item), "No")
        pets_allowed = next(("Yes" for item in ammenities if "pets" in item), "No")
        hair_dryer = next(("Yes" for item in ammenities if "hair dryer" in item), "No")
        heating = next(("Yes" for item in ammenities if "heating" in item), "No")
        refrigerator = next(("Yes" for item in ammenities if "refrigerator" in item), "No")
        stove = next(("Yes" for item in ammenities if "stove" in item), "No")
        oven = next(("Yes" for item in ammenities if "oven" in item), "No")
        coffee_maker = next(("Yes" for item in ammenities if "coffee maker" in item), "No")
        dining_table = next(("Yes" for item in ammenities if "dining table" in item), "No")
        self_check_in = next(("Yes" for item in ammenities if "self check-in" in item), "No")
        lockbox = next(("Yes" for item in ammenities if "lockbox" in item), "No")
        cooking_pots = next(("Yes" for item in ammenities if "pots" in item), "No")
        smoke_alarm = next(("Yes" for item in ammenities if "smoke alarm" in item), "No")
        co2_alarm = next(("Yes" for item in ammenities if "monoxide alarm" in item), "No")
        dish_washer = next(("Yes" for item in ammenities if "dishwasher" in item), "No")
        patio_and_balcony = next(("Yes" for item in ammenities if "patio" in item or "balcony" in item), "No")
        tv = next(("Yes" for item in ammenities if "tv" in item), "No")
        hot_kettle = next(("Yes" for item in ammenities if "kettle" in item), "No")

        users_review = [
            item.find("span", {"class": "lrl13de"}).text
            for item in listing_html.find("div", {"class": "_88xxct"}).find_all("div", {"class": "_b7zir4z"})
        ]
        review_1, review_2, review_3 = (users_review + [None] * 3)[:3]

        listing_data = {
            "city": city,
            "listing_id": int(listing_id),
            "title": listing_title,
            "guests": guests,
            "bathrooms": bathroom,
            "bedrooms": bedroom,
            "apartment_type": apartment_type,
            "price_per_night": price_per_night,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "star": stars,
            "number_of_reviews": no_of_reviews,
            "cleanliness": cleanliness,
            "accuracy": accuracy,
            "check_in": check_in,
            "communication": comm,
            "location": location,
            "value": value,
            "host_response_rate": host_response_rate,
            "bathtub": bathtub,
            "hot_water": hot_water,
            "hangers": hangers,
            "bed_linens": bed_linens,
            "iron": iron,
            "kitchen": kitchen,
            "wifi": wifi,
            "elevator": elevator,
            "washer": washer,
            "parking": parking,
            "workspace": workspace,
            "pets_allowed": pets_allowed,
            "hair_dryer": hair_dryer,
            "heating": heating,
            "refrigerator": refrigerator,
            "stove": stove,
            "oven": oven,
            "coffee_maker": coffee_maker,
            "dining_table": dining_table,
            "self_check_in": self_check_in,
            "lockbox": lockbox,
            "cooking_pots": cooking_pots,
            "smoke_alarm": smoke_alarm,
            "carbon_monoxide_alarm": co2_alarm,
            "dish_washer": dish_washer,
            "patio_or_balcony": patio_and_balcony,
            "television": tv,
            "hot_water_kettle": hot_kettle,
            "review_1": review_1,
            "review_2": review_2,
            "review_3": review_3
        }

        driver.quit()
        return listing_data

    def extract_data_from_url(listiing_urls: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """
        A function to extract listing data from Airbnb listing URLs.

        :param listiing_urls: Dictionary with key-value pairs of city name and list of listing URLs.
        :return: A list of dictionary containing extracted data.
        """
        listing_data = []

        logger.info("<<<<<<<<<<<<<<<<< Extracting Listing data ... >>>>>>>>>>>>>>>>>>>>>>>>")
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_data = {
                executor.submit(ExtractListingData.extract_and_transform_data, city, url):
                    (city, url) for city, urls in listiing_urls.items() for url in urls[:5]
            }

            for future in as_completed(future_to_data):
                city, url = future_to_data[future]
                try:
                    result = future.result()
                    listing_data.append(result)
                except Exception as e:
                    logger.error(f"An error occurred while fetching data for {city}: {e}")
                    logger.error(f"Failed URL: {url}")
        logger.info("<<<<<<<<<<<<<<<<< Listing data extraction completed. >>>>>>>>>>>>>>>>>>>>>>>>>>")
        return listing_data
