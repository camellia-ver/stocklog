import os
from dotenv import load_dotenv
from stock_collector.collector import create_stock_data_by_realtime
from stock_collector.utils import now_str, init_env, get_codes
from stock_collector.logger import logger

if __name__ == '__main__':
    init_env()

    today = now_str('%Y-%m-%d')
    codes = get_codes(today)
    duration_minutes = int(os.getenv("REALTIME_DURATION_MINUTES", 390))

    logger.info(f"[{now_str()}] 실시간 수집 시작: {duration_minutes}분 동안 실행됩니다.")
    create_stock_data_by_realtime(codes,duration_minutes)