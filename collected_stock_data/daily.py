from pykrx import stock
from stock_collector.collector import create_stock_data_by_daily
from stock_collector.utils import now_str, load_or_create_name_dict
import pandas as pd
import os

if __name__ == '__main__':
    os.makedirs("data/logs", exist_ok=True)
    os.makedirs("data/summary", exist_ok=True)

    today = now_str('%Y-%m-%d')
    kospi_codes = stock.get_market_ticker_list(today, market="KOSPI")
    kosdaq_codes = stock.get_market_ticker_list(today, market="KOSDAQ")

    codes_dict = {
        "KOSPI" : kospi_codes,
        "KOSDAQ" : kosdaq_codes
    }

    create_stock_data_by_daily(codes_dict, today)