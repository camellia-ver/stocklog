from datetime import datetime
import os
from pykrx import stock
import pandas as pd
from dotenv import load_dotenv
from .logger import logger
from .db import connect_db, save_stock_data_by_daily, save_stock_data_by_basic

load_dotenv()
CSV_DIRS = {
    "daily": os.getenv("CSV_DAILY_DIR", "data/summary"),
    "basic": os.getenv("CSV_BASIC_DIR", "data/basic")
}

def now_str(fmt='%Y-%m-%d %H:%M:%S') -> str:
    return datetime.now().strftime(fmt)

def init_env():
    data_dir = os.getenv("DATA_DIR", "data")
    log_dir = os.getenv("LOG_DIR", f"{data_dir}/logs")
    os.makedirs(log_dir, exist_ok=True)

    logger.info(f"[{now_str()}] 환경 초기화 완료. DATA_DIR={data_dir}, LOG_DIR={log_dir}")

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