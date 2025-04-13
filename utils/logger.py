import os
import logging
from dataclasses import dataclass

@dataclass

class LoggerHandler:
    """
    Logger utility class that configures and provides a reusable logger instance.

    This class sets up a logger that writes log messages to a file (`django_log.log`)
    with a specified maximum size (50 MB). If the log file exceeds the limit, it is deleted
    and recreated to prevent uncontrolled growth.

    Attributes:
        name (str): The name of the logger, defaults to the module name.
        log_file (str): Path to the log file.
        max_log_size (int): Maximum size (in bytes) allowed for the log file.

    Methods:
        get_logger(): Returns the configured logger instance.
    """
    name: str = __name__
    log_file: str = "django_log.log"
    max_log_size: int = 50 * 1024 * 1024  # 50 MB

    def __post_init__(self):
        self._check_log_size()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)


        file_handler = logging.FileHandler(self.log_file, mode="a")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def _check_log_size(self):
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_log_size:
            os.remove(self.log_file)

    def get_logger(self):
        return self.logger
