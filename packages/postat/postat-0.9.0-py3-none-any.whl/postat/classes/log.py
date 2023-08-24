import logging
import datetime
from typing import Optional
from enum import Enum

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class Logger:
    def __init__(self, name: Optional[str] = None, log_file: Optional[str] = None, level: LogLevel = LogLevel.WARNING):
        self.logger = logging.getLogger(name or __name__)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.set_log_level(level)

    def set_log_level(self, level: LogLevel):
        self.logger.setLevel(level.value)

    def log_message(self, message: str, level: LogLevel = LogLevel.INFO):
        if level == LogLevel.DEBUG:
            self.logger.debug(message)
        elif level == LogLevel.INFO:
            self.logger.info(message)
        elif level == LogLevel.WARNING:
            self.logger.warning(message)
        elif level == LogLevel.ERROR:
            self.logger.error(message)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(message)

    def log_debug(self, message: str):
        self.log_message(message, LogLevel.DEBUG)

    def log_info(self, message: str):
        self.log_message(message, LogLevel.INFO)

    def log_warning(self, message: str):
        self.log_message(message, LogLevel.WARNING)

    def log_error(self, message: str):
        self.log_message(message, LogLevel.ERROR)

    def log_critical(self, message: str):
        self.log_message(message, LogLevel.CRITICAL)