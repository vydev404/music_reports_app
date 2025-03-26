# -*- coding: utf-8 -*-
import logging
import sys

from processing.config import settings as config
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler


class Utf8StreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream or sys.stdout)
        self.stream = stream or sys.stdout
        self.stream.reconfigure(encoding="utf-8")


class Logger:
    def __init__(self, log_file, level=logging.INFO, log_type="BY_TIME"):
        self.logger_type = log_type
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        # Exclude handlers duplicating
        if not self.logger.hasHandlers():
            # Log format
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            if self.logger_type == "BY_TIME":
                # File rotation for log files by time
                file_handler = TimedRotatingFileHandler(
                    log_file,
                    when=config.logger.log_time,  # 'H' for hourly, 'midnight' for daily
                    interval=1,
                    backupCount=config.logger.log_backup_count,
                    encoding="utf-8",
                )
            elif self.logger_type == "BY_SIZE":
                file_handler = RotatingFileHandler(
                    filename=log_file,
                    maxBytes=config.logger.log_max_size,
                    encoding="utf-8",
                )
            else:
                file_handler = logging.FileHandler(
                    log_file, encoding="utf-8"
                )  # Default log file

            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # Console handler, for output logs to stdout
            console_handler = Utf8StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)
