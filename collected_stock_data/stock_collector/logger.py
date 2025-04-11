import logging
from logging.handlers import RotatingFileHandler
import os

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "log")

logger = logging.getLogger("stock_collector")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

info_handler = logging.FileHandler(os.path.join(LOG_DIR, 'info.log'))
info_handler.setLevel(logging.INFO)
info_handler.addFilter(LevelFilter(logging.INFO))
info_handler.setFormatter(formatter)

warning_handler = logging.FileHandler(os.path.join(LOG_DIR, 'warning.log'))
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(LevelFilter(logging.WARNING))
warning_handler.setFormatter(formatter)

error_handler = logging.FileHandler(os.path.join(LOG_DIR, 'error.log'))
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(LevelFilter(logging.ERROR))
error_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)

file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1 * 1024 * 1024, backupCount=3, encoding='utf-8'
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

__all__ = ["logger"]