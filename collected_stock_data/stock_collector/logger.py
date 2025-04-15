import logging
from logging.handlers import RotatingFileHandler
import os

# 특정 로그 레벨만 필터링하는 필터 클래스
class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

# 로그 디렉터리 생성
LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 순환 로그 파일 기본 이름
LOG_FILE = os.path.join(LOG_DIR, "log")

# 로거 생성
logger = logging.getLogger("stock_collector")
logger.setLevel(logging.DEBUG)

# 로그 포맷 설정
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

# INFO 로그 핸들러
info_handler = logging.FileHandler(
    os.path.join(LOG_DIR, 'info.log'), encoding='utf-8'
)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(LevelFilter(logging.INFO))
info_handler.setFormatter(formatter)

# WARNING 로그 핸들러
warning_handler = logging.FileHandler(
    os.path.join(LOG_DIR, 'warning.log'), encoding='utf-8'
)
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(LevelFilter(logging.WARNING))
warning_handler.setFormatter(formatter)

# ERROR 로그 핸들러
error_handler = logging.FileHandler(
    os.path.join(LOG_DIR, 'error.log'), encoding='utf-8'
)
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(LevelFilter(logging.ERROR))
error_handler.setFormatter(formatter)

# 콘솔 출력 핸들러
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 핸들러 등록
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)

__all__ = ["logger"]