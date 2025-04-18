from datetime import datetime
import os
import pandas as pd
from dotenv import load_dotenv
from .logger import logger
from .db import get_db_connection, save_daily_stock_data, save_basic_stock_data

load_dotenv()
CSV_DIRS = {
    "daily": os.getenv("CSV_DAILY_DIR", "data/summary"),
    "basic": os.getenv("CSV_BASIC_DIR", "data/basic")
}

def now_str(fmt='%Y-%m-%d %H:%M:%S') -> str:
    """
    현재 시간을 지정된 포맷의 문자열로 반환합니다.

    Args:
        fmt (str): datetime 포맷 문자열 (기본값: '%Y-%m-%d %H:%M:%S')

    Returns:
        str: 포맷된 현재 시간 문자열
    """
    return datetime.now().strftime(fmt)

def init_env():
    """
    환경 초기화를 수행합니다.
    로그 디렉토리를 생성하고 초기화 완료 로그를 출력합니다.
    """
    data_dir = os.getenv("DATA_DIR", "data")
    log_dir = os.getenv("LOG_DIR", f"{data_dir}/logs")
    os.makedirs(log_dir, exist_ok=True)

    logger.info(f"[{now_str()}] 환경 초기화 완료. DATA_DIR={data_dir}, LOG_DIR={log_dir}")

def save_to_csv(df: pd.DataFrame, now_str_value: str, collect_type: str) -> None:
    """
    수집된 데이터를 CSV 파일로 저장합니다.

    Args:
        df (pd.DataFrame): 저장할 데이터 프레임
        now_str_value (str): 저장 시점 문자열 (파일명에 사용됨)
        collect_type (str): 수집 데이터 종류 ('daily' 또는 'basic')

    Notes:
        유효하지 않은 collect_type인 경우 경고 로그를 출력하고 종료합니다.
    """
    save_path = CSV_DIRS.get(collect_type)

    if not save_path:
        logger.warning(f"❌ 잘못된 저장 타입: {collect_type}")
        return
    
    os.makedirs(save_path, exist_ok=True)

    filename_type = {
        "daily": "summary_data",
        "basic": "basic_data"
    }.get(collect_type, "data")

    filename = f"{save_path}/{filename_type}_{now_str_value}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')

def save_to_db(df: pd.DataFrame, collect_type: str) -> None:
    """
    수집된 데이터를 데이터베이스에 저장합니다.

    Args:
        df (pd.DataFrame): 저장할 데이터 프레임
        collect_type (str): 수집 데이터 종류 ('daily' 또는 'basic')

    Notes:
        DB 연결 실패 시 오류 로그를 출력하고 종료하며, 
        잘못된 collect_type인 경우에도 경고 로그를 출력합니다.
    """
    connection = None
    try:
        connection = get_db_connection()
    except Exception as e:
        logger.error(f"❌ DB 연결 실패: {e}")

    save_funcs = {
        "daily": save_daily_stock_data,
        "basic": save_basic_stock_data
    }

    if connection and collect_type in save_funcs:
        try:
            save_funcs[collect_type](df, connection)
        finally:
            connection.close()
    else:
        logger.warning(f"❌ 잘못된 수집 타입 또는 DB 연결 실패: {collect_type}")
