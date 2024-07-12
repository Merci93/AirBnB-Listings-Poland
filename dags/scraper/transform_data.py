"""Module to extract data from html and transform into a pandas dataframe."""

from datetime import date
from typing import Any, Union

from tqdm import tqdm
from unidecode import unidecode


class ExtractData:
    """Perform data extraction and transformation form HTML data."""

    @staticmethod
    def extract_and_transform_data(html_data: Union[str, Any]) -> Union[dict, str]:
        """
        Extract listing data from the return HTML object, and return list of dictionaries with extracted data.

        :param html_data: HTML data in a list.
        """
        listing_data = []

        html_list = [(item[0], item[1]) for sublist in html_data for item in sublist]
        for city_html in tqdm(html_list):
            listings = city_html[1].find_all("div", {"class": "c4mnd7m"})
            for list_detail in listings:
                city = city_html[0]
                try:
                    title = unidecode(list_detail.find("div", {"data-testid": "listing-card-title"}).text)
                except AttributeError:
                    title = "N/A"
                try:
                    subtitle = unidecode(list_detail.find("span", {"data-testid": "listing-card-name"}).text)
                except AttributeError:
                    subtitle = "N/A"
                other_details = [item.text for item in list_detail.find_all("span", {"class": "dir dir-ltr"})]
                bed_types = "N/A"
                availability = "N/A"
                for item in other_details:
                    if "bed" in item or "beds" in item:
                        bed_types = item
                    if "–" in item:
                        availability = item.replace("–", "-")
                try:
                    stars = list_detail.find("span", {"class": "r1dxllyb"}).text.split("(")[0].strip()
                except AttributeError as e:
                    stars = str(e)
                try:
                    no_of_ratings = list_detail.find("span",
                                                     {"class": "r1dxllyb"}).text.split("(")[1].strip().replace(")", "")
                except (IndexError, AttributeError):
                    no_of_ratings = stars
                try:
                    total_price = list_detail.find("div", {"class": "_tt122m"}).text.split("zł")[0].strip()
                except AttributeError:
                    total_price = "N/A"
                try:
                    get_price = list_detail.find("span", {"class": "_14y1gc"}).text
                    if "originally" in str(get_price):
                        price_per_night = get_price.split("zł")[1].strip()
                        original_price = get_price.split("zł")[0].strip()
                    else:
                        price_per_night = get_price.split("zł")[0].strip()
                        original_price = price_per_night
                except AttributeError:
                    price_per_night = "N/A"
                    original_price = "N/A"

                listing_data.append({"city": city,
                                     "date": date.today(),
                                     "title": title,
                                     "subtitle": subtitle,
                                     "bed_type": bed_types,
                                     "price_per_night (zl)": price_per_night,
                                     "original_price (zl)": original_price,
                                     "total_price (zl)": total_price,
                                     "availability": availability,
                                     "star": stars,
                                     "number_of_ratings": no_of_ratings,
                                     })
        return listing_data
