from .utils import now_str, get_daily_summary_stock_data, get_stock_basic_data
from .db import connect_db, save_stock_data_by_daily, save_stock_data_by_basic
from .logger import logger
import pandas as pd
from datetime import datetime
import os, time
from pykrx import stock
from dotenv import load_dotenv

load_dotenv()
CSV_DIRS = {
    "daily": os.getenv("CSV_DAILY_DIR", "data/summary"),
    "basic": os.getenv("CSV_BASIC_DIR", "data/basic")
}

def create_stock_data_by_daily(codes:list, date: str):
    all_data = []

    for code in codes:
        try:
            logger.info(f"{code} 처리 중")
                
            merged = get_daily_summary_stock_data(date, code)  
            merged.reset_index(inplace=True)
            merged['종목코드'] = code

            all_data.append(merged)
        except Exception as e:
            logger.info(f"{code}에서 오류 발생: {e}")
    
    if all_data:
        result_df = pd.concat(all_data, ignore_index=True)
        save_to_csv(result_df,date,"daily")
        save_to_db(result_df, "daily")
    else:
        logger.warning("수집된 데이터가 없습니다.")

def create_stock_data_by_basic():
    stock_list = get_stock_basic_data()
    stock_df = pd.DataFrame(stock_list)
    
    save_to_csv(stock_df, now_str('%Y_%m_%d'), "basic")
    save_to_db(stock_df, "basic")

def save_to_csv(df: pd.DataFrame, now: str, collect_type: str) -> None:
    path = CSV_DIRS.get(collect_type)

    if not path:
        logger.warning(f"❌ 잘못된 저장 타입: {collect_type}")
        return
    
    os.makedirs(path, exist_ok=True)

    filename_type = {
        "daily": "summary_data",
        "basic": "basic_data"
    }.get(collect_type, "data")

    filename = f"{path}/{filename_type}_{now}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')

def save_to_db(df: pd.DataFrame, collect_type: str) -> None:
    db_connect = None
    try:
        db_connect = connect_db()
    except Exception as e:
        logger.error(f"❌ DB 연결 실패: {e}")

    save_funcs = {
        "daily": save_stock_data_by_daily,
        "basic": save_stock_data_by_basic
    }

    if db_connect and collect_type in save_funcs:
        try:
            save_funcs[collect_type](df, db_connect)
        finally:
            db_connect.close()
    else:
        logger.warning(f"❌ 잘못된 수집 타입 또는 DB 연결 실패: {collect_type}")