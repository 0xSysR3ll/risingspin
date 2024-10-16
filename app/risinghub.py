import re

from typing import Dict, Optional
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from app.logger import Logger

logger = Logger(name=__name__)

class RisingHub:
    """
    Class for interacting with RisingHub.

    Attributes:
        BASE_URL (str): The base URL of the RisingHub website.
        PROFILE_URL (str): The URL of the profile page.
        LOGIN_URL (str): The URL of the login page.
        SPIN_URL (str): The URL of the roulette page.
        SPIN_REGEX (re.Pattern): A regular expression to extract
        the next spin time from the roulette page.
    """
    BASE_URL = "https://risinghub.net"
    PROFILE_URL = BASE_URL + "/profile"
    LOGIN_URL = BASE_URL + "/login"
    SPIN_URL = BASE_URL + "/roulette"
    SPIN_REGEX = re.compile(r"([0-9]{1,2}\.?[0-9]{1,2}) hours")

    def __init__(self, username: str, password: str) -> None:
        """
        Initialize the class with the provided credentials.

        Args:
            username (str): The username to log in with.
            password (str): The password to log in with.
        """
        self.username = username
        self.password = password
        self.session = requests.Session()

    def get_token(self, page_url: str) -> str:
        """
        Get CSRF token required for form submission.

        Args:
            page_url (str): The URL of the page to get the CSRF token from.

        Returns:
            str: The CSRF token.
        """
        try:
            response = self.session.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            token = soup.find("input", {"name": "_token"}).get("value")
            return token
        except requests.RequestException as e:
            logger.error(f"[-] Error while fetching token: {e}")
            exit(1)

    def login(self) -> None:
        """
        Log in to the website with the provided credentials.
        """
        token = self.get_token(self.LOGIN_URL)
        login_data = {
            "username": self.username,
            "password": self.password,
            "_token": token,
            "submit": ""
        }
        try:
            response = self.session.post(self.LOGIN_URL, data=login_data)
            response.raise_for_status()
            if '/login' in response.text:
                logger.error("[-] Login failed")
                exit(1)
            logger.info("[+] Login success!")
        except requests.RequestException as e:
            logger.error(f"[-] Error during login: {e}")
            exit(1)

    def get_heroes(self) -> Dict[str, str]:
        """
        Fetch heroes for the spin.

        Returns:
            dict: A dictionary containing the heroes available
        """
        try:
            response = self.session.get(self.SPIN_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            # Check if heroes are available
            select = soup.find("select", {"name": "hero"})
            if not select:
                return {}
            heroes = {  # pylint: disable=redefined-outer-name
                hero.get("value"): hero.text
                for hero in select.find_all("option")}
            return heroes
        except requests.RequestException as e:
            logger.error(f"[-] Error while fetching heroes: {e}")
        return {}

    def spin(self, hero: int) -> datetime:
        """
        Perform a spin and return the next available spin time.

        Args:
            hero (int): The hero to spin with.

        Returns:
            datetime: The next available spin time.
        """
        token = self.get_token(self.SPIN_URL)
        spin_data = {"hero": hero, "_token": token, "submit": ""}
        try:
            if hero != 0:
                spin_response = self.session.post(
                    self.SPIN_URL, data=spin_data)
                spin_response.raise_for_status()
            # After the spin, check when the next spin will be available
            result_page = self.session.get(self.SPIN_URL).text
            hour_match = self.SPIN_REGEX.search(result_page)
            if hour_match:
                next_spin_in = float(hour_match.group(1))
                delta = timedelta(hours=next_spin_in)
                next_spin_time = datetime.now() + delta  # pylint: disable=redefined-outer-name
            else:
                next_spin_time = datetime.now() + timedelta(hours=1) # pylint: disable=redefined-outer-name
                logger.warning("[-] Could not find the next spin time in the response.")
            return next_spin_time
        except requests.RequestException as e:
            logger.error(f"[-] Error during spin: {e}")
        return None

    def get_item_won(self, username: str) -> Optional[Dict[str, str]]:  # pylint: disable=redefined-outer-name
        """
        Get the item won in the daily spin.

        Args:
            username (str): The username of the user who won the item.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the item name, quantity and URL,
                or None if no item is found.
        """

        username = username.lower()
        prizes_page = self.session.get(self.SPIN_URL).text
        
        soup = BeautifulSoup(prizes_page, "html.parser")

        # Find the relevant divs
        divs = soup.find_all(
            "div", class_="content callout-secondary", recursive=True)

        # Iterate over the divs
        for div in divs:
            # Find all the images in the div
            images = div.find_all("img")

            # Iterate over the images
            for image in images:
                # Get the title of the image
                title = image.get("title").replace("\n", " ").lower()

                # Check if the username is in the title
                if username.lower() in title:
                    # Get the quantity and item name from the title
                    quantity = title.split()[0].strip()
                    item_name = title.split(username)[
                        0].split(quantity)[1].strip()

                    # Get the URL of the item
                    item_url = image.get("src")

                    # Return the item information
                    return {
                        "item": item_name,
                        "quantity": quantity,
                        "item_url": item_url,
                    }

        # Return None if no item is found
        return None

    def close_session(self) -> None:
        """
        Close the session after operations are complete.
        """
        self.session.close()
