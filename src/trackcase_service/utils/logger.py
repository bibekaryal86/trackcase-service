import datetime
import logging
import sys

import pytz


class Logger:
    def __init__(self, logger: logging.Logger, module_name: str):
        self.logger = logger
        self.logger.setLevel(logging.INFO)

        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setLevel(logging.INFO)

        self.formatter = logging.Formatter(
            f"[%(asctime)s] [trackcase-service] [{module_name}] "
            f"[%(threadName)s] [%(levelname)s] %(message)s"
        )

        def converter(timestamp):
            dt = datetime.datetime.fromtimestamp(timestamp)
            return pytz.timezone("America/Denver").localize(dt).timetuple()

        self.formatter.converter = converter
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def set_level(self, level):
        self.logger.setLevel(level)
        self.handler.setLevel(level)
