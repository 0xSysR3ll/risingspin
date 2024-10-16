import logging
from colorama import Fore, init

init(autoreset=True)


class Logger:
    """A simple logger with colors"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message: str) -> None:
        """Log a debug message with blue color"""
        self._log(logging.DEBUG, message, Fore.BLUE)

    def info(self, message: str) -> None:
        """Log an info message with green color"""
        self._log(logging.INFO, message, Fore.GREEN)
    def success(self, message: str) -> None:
        """Log a success message with green color"""
        self._log(logging.INFO, message, Fore.GREEN)
    def warning(self, message: str) -> None:
        """Log a warning message with yellow color"""
        self._log(logging.WARNING, message, Fore.YELLOW)

    def error(self, message: str) -> None:
        """Log an error message with red color"""
        self._log(logging.ERROR, message, Fore.RED)

    def _log(self, level: int, message: str, color: str) -> None:
        """Internal helper for logging with colors"""
        self.logger.log(level, "%s%s%s", color, message, Fore.RESET)
