from datetime import datetime
import json, os
from pykrx import stock
import pandas as pd
from dotenv import load_dotenv
from .logger import logger

def get_market_codes(date_str: str) -> dict:
    try:
        return {
            "KOSPI" : stock.get_market_ticker_list(date_str, market="KOSPI"),
            "KOSDAQ" : stock.get_market_ticker_list(date_str, market="KOSDAQ")
        }
    except Exception as e:
        logger.error(f"[get_market_codes] 오류 발생: {e}")
        return {}

def get_stock_data(date: str, code: str) -> pd.DataFrame:
    ohlcv = stock.get_market_ohlcv_by_date(date,date,code)
    fundamental = stock.get_market_fundamental_by_date(date,date,code)

    if ohlcv.empty or fundamental.empty:
        logger.warning(f"[get_stock_data] 데이터 없음: {code} - {date}")
        return pd.DataFrame()

    logger.info(f"[get_stock_data] 데이터 수집 성공: {code} - {date}")
    return pd.concat([ohlcv, fundamental], axis=1)

def now_str(fmt='%Y-%m-%d %H:%M:%S') -> str:
    return datetime.now().strftime(fmt)

def load_or_create_name_dict(filepath="data/name_dict.json") -> dict:
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"[load_or_create_name_dict] 파일 로드 실패: {e}")
        
    name_dict = get_name_dict()

    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding="utf-8") as f:
            json.dump(name_dict, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"[load_or_create_name_dict] 파일 저장 실패: {e}")

    return name_dict

def get_name_dict(date_str=None):
    if not date_str:
        date_str = datetime.today().strftime('%Y%m%d')

    name_dict = {}
    try:
        for market in ("KOSPI","KOSDAQ"):
            codes = stock.get_market_ticker_list(date_str, market=market)
            for code in codes:
                name_dict[code] = stock.get_market_ticker_name(code)
    except Exception as e:
        logger.error(f"[get_name_dict] 종목명 수집 실패: {e}") 
        return {}   
    
    return name_dict

def init_env():
    load_dotenv()
    data_dir = os.getenv("DATA_DIR", "data")
    log_dir = os.getenv("LOG_DIR", f"{data_dir}/logs")
    os.makedirs(log_dir, exist_ok=True)

    logger.info(f"[{now_str()}] 환경 초기화 완료. DATA_DIR={data_dir}, LOG_DIR={log_dir}")