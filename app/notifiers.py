from datetime import datetime
import requests

from app.logger import Logger

logger = Logger(name=__name__)

class Discord(object):
    def __init__(self, webhook_url: str) -> None:
        """
        Initialize the Discord notifier with the provided webhook URL.

        Args:
            webhook_url (str): The URL of the Discord webhook to send notifications to.
        """
        self.webhook_url = webhook_url

    def notify(self, hero_name: str, prize: dict, next_spin_time: datetime) -> None:
        """
        Send a Discord notification with the prize won and the next available spin time.

        Args:
            hero_name (str): The name of the hero who won the prize.
            prize (dict): A dictionary containing the prize information, with the following keys:
                "item": str, the name of the item won
                "quantity": int, the number of items won
                "item_url": str, the URL of the item image
            next_spin_time (datetime): The next available spin time
        """
        data = {
        "content": None,
        "embeds": [
            {
                "title": f"Just won {prize['quantity']}x {prize['item']} today !",
                "description": f"Next available spin will be {next_spin_time.strftime('%A at %H:%M:%S')}",
                "color": 59201,
                "author": {
                    "name": hero_name.capitalize()
                },
                "image": {
                    "url": f"https://risinghub.net{prize['item_url']}"
                },
                "thumbnail": {
                    "url": "https://risinghub.net/images/rh_logo.png"
                }
            }
        ],
        "username": "Rising Hub Auto-Spin",
        "attachments": []
    }
        try:
            response = requests.post(url=self.webhook_url, json=data, timeout=10)
            if response.status_code == 204:
                logger.info("[+] Notification sent !")
            else:
                logger.warning(f"[-] Error while sending notification: {response.text}")
        except requests.RequestException as e:
            logger.error(f"[-] Error while sending notification: {e}")