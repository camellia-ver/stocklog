from datetime import datetime
import os
from pykrx import stock
import pandas as pd
from dotenv import load_dotenv
from .logger import logger

load_dotenv()

def get_codes(date_str: str) -> list:
    try:
        return stock.get_market_ticker_list(date_str, market="ALL")
    except Exception as e:
        logger.error(f"[get_codes] 오류 발생: {e}")
        return []

def get_daily_summary_stock_data(date: str, code: str) -> pd.DataFrame:
    ohlcv = stock.get_market_ohlcv_by_date(date,date,code)
    fundamental = stock.get_market_fundamental_by_date(date,date,code)

    if ohlcv.empty or fundamental.empty:
        logger.warning(f"[get_daily_summary_stock_data] 데이터 없음: {code} - {date}")
        return pd.DataFrame()

    logger.info(f"[get_daily_summary_stock_data] 데이터 수집 성공: {code} - {date}")
    return pd.concat([ohlcv, fundamental], axis=1)

def now_str(fmt='%Y-%m-%d %H:%M:%S') -> str:
    return datetime.now().strftime(fmt)

def init_env():
    data_dir = os.getenv("DATA_DIR", "data")
    log_dir = os.getenv("LOG_DIR", f"{data_dir}/logs")
    os.makedirs(log_dir, exist_ok=True)

    logger.info(f"[{now_str()}] 환경 초기화 완료. DATA_DIR={data_dir}, LOG_DIR={log_dir}")

def get_stock_basic_data(date_str=None) -> list:
    if not date_str:
        date_str = datetime.today().strftime('%Y%m%d')

    stock_list = []

    try:
        for market in ("KOSPI","KOSDAQ"):
            codes = stock.get_market_ticker_list(date_str, market=market)
            for code in codes:
                name = stock.get_market_ticker_name(code)
                stock_list.append(
                    {
                        "종목코드": code,
                        "종목명": name,
                        "구분": market
                    }
                )
    except Exception as e:
        logger.error(f"[get_stock_basic_data] 종목명 수집 실패 {type(e).__name__}: {e}")
        return []  
    
    return stock_list