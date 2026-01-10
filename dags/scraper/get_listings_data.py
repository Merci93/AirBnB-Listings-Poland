"""Scrapes select data from the given URL, specifically written to extract data from AirBnB webpage."""
import re
from datetime import datetime
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from scraper.log_handler import logger
# from scraper.selenium_driver import init_driver
from log_handler import logger
from selenium_driver import init_driver


class ExtractListingData:
    """
    Extract structured listing data from listing URL.
    """
    def __init__(self, city: str, listing_urls: List[str], debug: bool = False):
        """
        Initialize ExtractListingData class

        :param city: City name
        :param listing_urls: URL for each listing found per city
        :param debug: Flag to initilaize webdriver in debug mode
        """
        self.city = city
        self.listing_urls = listing_urls
        self.debug = debug
        self.driver = init_driver(debug=debug)
        self.wait = WebDriverWait(self.driver, 15)

    def extract_listings(self) -> List[Dict[str, Any]]:
        """
        A function to extract listing data from listing URL.

        :return: _description_
        """
        results = []

        try:
            logger.info("Extracting listing data for city %s ...", self.city)

            for url in self.listing_urls:
                try:
                    data = self._extract_single_listing(url)
                    results.append(data)

                except RuntimeError as exc:
                    logger.error("Blocked or schema change detected: %s", exc)
                    break  # stop entire city batch

                except Exception as exc:
                    logger.exception("Failed listing extraction %s: %s", url, exc)

        finally:
            self.driver.quit()
            logger.info("Data Extraction completed. Webdriver terminated.")

        return results

    def _extract_single_listing(self, url: str) -> Dict[str, Any]:
        self.driver.get(url)

        self._dismiss_popups()
        # self._assert_not_blocked()

        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )

        bs_listing_html = BeautifulSoup(self.driver.page_source, "html.parser")

        listing_id = url.split("?")[0].rsplit("/", 1)[-1]
        title = bs_listing_html.title.text.strip() if bs_listing_html.title else "N/A"

        listing_price = self._extract_price(bs_listing_html)
        specs = self._extract_specs(bs_listing_html)
        ratings = self._extract_ratings(bs_listing_html)
        amenities = self._extract_amenities()

        return {
            "city": self.city,
            "listing_id": int(listing_id),
            "title": title,
            "price": listing_price,
            **specs,
            **ratings,
            **amenities,
            "url": url,
            "date_pulled": datetime.today().strftime('%Y-%m-%d')
        }

    def _close_translation_notification(self) -> None:
        pass

    def _assert_not_blocked(self) -> None:
        page_text = self.driver.page_source.lower()
        if "captcha" in page_text or "verify" in page_text:
            raise RuntimeError("Captcha or bot verification detected")

    def _dismiss_popups(self) -> None:
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
            ).click()
        except Exception:
            pass

    def _extract_price(self, bs_listing_html: BeautifulSoup) -> str:
        """Extract listing price."""
        rating_text = bs_listing_html.get_text(" ").lower()

        match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*(zł)', rating_text)
        if not match:
            return "N/A"

        return f"{match.group(1)} {match.group(2)}"

    def _extract_specs(self, bs_listing_html: BeautifulSoup) -> Dict[str, Any]:
        """Extract specifications for each listing."""

        text_blocks = [(li.get_text(separator=" ") or "").lower().strip() for li in bs_listing_html.find_all("li")]

        def extract_number(patterns: list[str], block_contains_shared: bool = False):
            for block in text_blocks:
                for pattern in patterns:
                    if re.search(rf"\b{pattern}\b", block):
                        shared = block_contains_shared and "shared" in block
                        match = re.search(r"(\d+)", block)
                        return (int(match.group(1)), shared) if match else ("N/A", shared)
            return "N/A", False

        guests, _ = extract_number(["guest", "guests"])
        bedrooms, shared_bedroom = extract_number(["bedroom", "bedrooms"], block_contains_shared=True)
        beds, _ = extract_number(["bed", "beds"])
        bathrooms, shared_bathroom = extract_number(["bath", "baths"], block_contains_shared=True)

        property_type = "studio" if any("studio" in t for t in text_blocks) else "N/A"

        return {
            "guests": guests,
            "bedrooms": bedrooms,
            "shared_bedroom": shared_bedroom,
            "beds": beds,
            "bathrooms": bathrooms,
            "shared_bathroom": shared_bathroom,
            "property_type": property_type,
        }

    def _extract_ratings(self, bs_listing_html: BeautifulSoup) -> Dict[str, Any]:
        """Extract ratings for each listing."""
        rating_text = bs_listing_html.get_text(" ").lower()

        def extract_float(label: str):
            match = re.search(rf"{label}.*?(\d\.\d)", rating_text)
            return float(match.group(1)) if match else "N/A"

        def extract_int(label: str):
            match = re.search(rf"(\d+)\s+{re.escape(label)}\b", rating_text, re.IGNORECASE)
            return int(match.group(1)) if match else "N/A"

        return {
            "overall_rating": extract_float("rated"),
            "cleanliness": extract_float("cleanliness"),
            "accuracy": extract_float("accuracy"),
            "communication": extract_float("communication"),
            "location": extract_float("location"),
            "value": extract_float("value"),
            "check_in": extract_float("check-in"),
            "reviews": extract_int("reviews"),
            "nights": extract_int("nights")
        }

    def _extract_amenities(self) -> Dict[str, Any]:
        """Extract ammenities of each listing."""
        try:
            button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[starts-with(., 'Show all')]")
                )
            )
            button.click()
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section"))
            )
        except Exception:
            return {}

        bs_listing_html = BeautifulSoup(self.driver.page_source, "html.parser")
        amenities = {div.text.lower() for div in bs_listing_html.select("section div")}

        def has(term: str):
            return "Yes" if any(term in a for a in amenities) else "No"

        return {
            "wifi": has("wifi"),
            "kitchen": has("kitchen"),
            "washer": has("washer"),
            "parking": has("parking"),
            "air_conditioning": has("air conditioning"),
            "heating": has("heating"),
            "tv": has("tv"),
            "pets_allowed": has("pets"),
            "refrigerator": has("refrigerator"),
        }

    def _extract_customer_comments(self, bs_listing_html: BeautifulSoup, limit: int = 3) -> List[str]:
        """Extract user review comments from listing HTML (mixed-case text)."""
        comments = []

        listings_text = bs_listing_html.get_text(" ")
        normalized_text = re.sub(r'\s+', ' ', listings_text)

        review_split = re.split(r"\b\d+\s+years\s+on\s+airbnb\b", normalized_text, flags=re.IGNORECASE)

        for text_block in review_split[1:]:
            if len(comments) >= limit:
                break

            # Cut off at the end of review section
            text_block = re.split(
                r"\b(show more|show all reviews|how reviews work|meet your host|where you’ll be)\b",
                text_block, flags=re.IGNORECASE
            )[0]

            # Remove rating and date metadata
            text_block = re.sub(r"Rating,\s*\d+(\.\d+)?\s*stars\s*,?", "", text_block, flags=re.IGNORECASE)
            text_block = re.sub(r"·\s*[A-Za-z]+\s+\d{4}", "", text_block)
            text_block = re.sub(r"·\s*Stayed\s+.*?(?=\w|$)", "", text_block, flags=re.IGNORECASE)

            text_block = text_block.strip(" ,.-")

            # Heuristic: require minimum word count
            if len(text_block.split()) >= 12:
                comments.append(text_block.strip())

        return comments
