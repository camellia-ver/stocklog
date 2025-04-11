from pykrx import stock
from stock_collector.collector import create_stock_data_by_daily
from stock_collector.utils import now_str, load_or_create_name_dict, get_market_codes, init_env
import os
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "data")
LOG_DIR = os.getenv("LOG_DIR", f"{DATA_DIR}/logs")

if __name__ == '__main__':
    init_env()

    today = now_str('%Y-%m-%d')
    codes_dict = get_market_codes(today)
    create_stock_data_by_daily(codes_dict, today)