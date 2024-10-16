"""

This module is used to load the configuration from a predefined file.

"""

import yaml
from app.logger import Logger

logger = Logger(name=__name__)


class Config():

    """

    This class is used to load the configuration from a predefined file.

    """

    def __init__(self, config_file: str = "config/config.yml"):
        """
        Initialize the class with the config file

        This method opens the config file and loads the configuration
        into the class as an attribute.

        The config file is assumed to be in YAML format.

        Example:
            config = Config()
        """

        self.notify: bool
        self.webhook_url: str
        self.username: str
        self.password: str
        self.random_hero: bool
        self.heroes: list

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = {}
            logger.warning("[-] Config file not found")
            exit(1)
        except yaml.YAMLError as e:
            logger.error(f"[-] Error loading config file: {e}")
            exit(1)

    def load(self):
        """
        Load the configuration into the class

        This method takes the configuration and loads it into the class as attributes.
        This allows you to access the configuration with dot notation.

        Example:
            config = Config()
            config.load()
            print(config.log_level)  # prints the log level
        """
        try:
            for key, value in self.config.items():
                setattr(self, key, value)
        except AttributeError as e:
            logger.error(f"[-] Error loading config: {e}")
            exit(1)
