#!/usr/bin/env python3
"""
Automated RisingHub Roulette

Copyright 2024 - 0xsysr3ll
"""

import random
import time
from datetime import datetime
from colorama import Fore, init
from app.risinghub import RisingHub
from app.logger import Logger
from app.notifiers import Discord
from app.config import Config

# Load logger
logger = Logger(name=__name__)

# Initialize colorama
init(autoreset=True)

# Load config variables
config = Config(config_file="config/config.yml")
config.load()

NOTIFY: bool = config.notify
WEBHOOK_URL: str = config.webhook_url
RANDOM_HERO: bool = config.random_hero
HEROES: list = config.heroes

def print_banner() -> None:
    """
    Print a banner with colors.
    """
    banner = f"""
{Fore.CYAN}   @@+.  .:#@
    @ +++=++++*:= @
  @ ++*+++++.   .*- @
 @:+++*+.       **+..@
@ ++ *-  .@@+   ++*+= @
@.+++*. *@@@@@  .****.@
@.++*+. .@@@@#  .****.@
@.-+***        .*****-@
 @.***++--..:***+=.+:@@
  @+.******#**:-*#.%@@
     @ :#*-.=*...@@@
        @@@@@@@@@

{Fore.LIGHTYELLOW_EX}Automated RisingHub Roulette
{Fore.LIGHTYELLOW_EX}Copyright 2024 - 0xsysr3ll
"""

    print(banner)


if __name__ == "__main__":
    # Print the banner
    print_banner()

    # Fetch credentials from environment variables for security
    USERNAME: str = config.username
    PASSWORD: str = config.password

    # Main loop for automated spinning
    while True:
        logger.debug("[*] Logging in...")
        rising_hub = RisingHub(
            username=USERNAME,
            password=config.password
        )
        rising_hub.login()
        # Check if heroes are available
        wanted_heroes = [wanted_hero.lower() for wanted_hero in HEROES]
        heroes = rising_hub.get_heroes()
        if len(wanted_heroes) > 0:
            logger.debug(f"[*] Filtering heroes to {wanted_heroes}...")
            for _, hero in heroes.copy().items():
                if hero.lower() not in wanted_heroes:
                    heroes.pop(_)
        prize: dict = {}
        next_spin_time: datetime = None
        try:
            # Heroes are available, choose one and spin
            hero = random.choice(list(heroes.keys()))
            hero_name = heroes[hero]
            logger.debug(f"[*] Spinning {hero_name}'s roulette...")
            next_spin_time = rising_hub.spin(
                hero)
            logger.info(f"[+] Spun {hero_name}'s roulette!")
            prize = rising_hub.get_item_won(username=USERNAME)
        except IndexError:
            # Spin is not available, get the next available spin time
            logger.warning("[-] Spin not available, getting next spin time...")
            next_spin_time = rising_hub.spin(0)
        except TypeError as e:
            logger.error(f"[-] Error while getting prize: {e}")
            prize = rising_hub.get_item_won(username=USERNAME)
        
        if len(prize) > 0:
            logger.info(
                f"[+] You just won {prize['quantity']}x {prize['item']} !")
            if NOTIFY:
                logger.debug("[*] Sending notification...")
                webhook_url = WEBHOOK_URL.replace('"', '').replace("'", "")
                discord = Discord(webhook_url=WEBHOOK_URL)
                discord.notify(
                    hero_name=hero_name,
                    prize=prize,
                    next_spin_time=next_spin_time if next_spin_time else "Unknown"
                )

        # Format the next spin time to "hh:mm:ss dd/mm/YYYY"
        logger.debug(
            f"[*] Next spin time: {next_spin_time.strftime('%A at %H:%M:%S')}")

        # Close the session
        rising_hub.close_session()

        # Wait until the next spin time
        try:
            time_to_wait = (next_spin_time - datetime.now()).total_seconds()
        except TypeError as e:
            logger.error(f"[-] Error while calculating time to wait: {e}")
            time_to_wait = 0
        if time_to_wait > 0:
            logger.debug(
                f"[*] Waiting {time_to_wait / 60:.2f} minutes until the next spin...")
            time.sleep(time_to_wait + 10)
        else:
            logger.debug("[*] Spinning immediately...")
