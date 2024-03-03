import datetime
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import pytz

from src.trackcase_service.utils.constants import REPO_HOME


class Logger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.setLevel(logging.INFO)

        # console logger
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setLevel(logging.INFO)

        self.formatter = logging.Formatter(
            "[%(asctime)s][trackcase-service][%(name)s]"
            "[%(levelname)s] [MESSAGE: %(message)s] | [EXTRA: %(extra)s] | [EXCEPTION: %(exc_info)s]"
        )

        def converter(timestamp):
            dt = datetime.datetime.fromtimestamp(timestamp)
            return pytz.timezone("America/Denver").localize(dt).timetuple()

        self.formatter.converter = converter
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.stream_handler)

        # file logger
        if REPO_HOME is not None and str(REPO_HOME).strip() != "":
            log_file_location = (
                REPO_HOME + "/logs/trackcase-service/trackcase-service.log"
            )
            log_dir = os.path.dirname(log_file_location)
            os.makedirs(log_dir, exist_ok=True)
            self.file_handler = TimedRotatingFileHandler(
                log_file_location,
                when="midnight",
                interval=1,  # Daily rotation
                backupCount=14,  # Keep logs for 14 days
                encoding="utf-8",
                delay=True,
            )
            self.file_handler.setLevel(logging.INFO)
            # if file logger is present, set console logger level at ERROR
            self.stream_handler.setLevel(logging.ERROR)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra={"extra": extra})

    def info(self, msg, extra=None):
        self.logger.info(msg, extra={"extra": extra})

    def error(self, msg, extra=None, exc_info=None):
        self.logger.error(msg, extra={"extra": extra}, exc_info=exc_info)
