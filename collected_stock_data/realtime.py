# 병렬처리로 구조개선 하기

from stock_collector.collector import create_stock_data_by_realtime
from pykrx import stock
from datetime import datetime
import os

if __name__ == '__main__':
    os.makedirs("data/logs", exist_ok=True)
    os.makedirs("data/prices", exist_ok=True)

    kospi_codes = stock.get_market_ticker_list(datetime.today().strftime('%Y%m%d'), market="KOSPI")
    kosdaq_codes = stock.get_market_ticker_list(datetime.today().strftime('%Y%m%d'), market="KOSDAQ")

    codes_dict = {
        "KOSPI" : kospi_codes,
        "KOSDAQ" : kosdaq_codes
    }
    duration_minutes = 2 #60 * 24 # 실행하고 싶은 시간(단위:분)

    create_stock_data_by_realtime(codes_dict,duration_minutes)