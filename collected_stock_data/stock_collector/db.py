import pymysql
from pymysql import cursors
from dotenv import load_dotenv
from typing import List,Dict
import os
from .logger import logger

def connect_db() -> pymysql.connections.Connection:
    try:
        load_dotenv()

        db_connect = pymysql.connect(
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            db=os.getenv("DB_NAME"),
            charset='utf8'
        )

        return db_connect
    except Exception as e:
        logger.info(f"DB 연결 실패: {e}")
        return None

def save_stock_data_by_daily(datas: List[Dict], db_connect: pymysql.connections.Connection):
    cursor = db_connect.cursor(cursors.DictCursor)

    insert_query = """INSERT INTO dailysummarystock(
        date, open_price, high_price, low_price, close_price, 
        volume, per, pbr, eps, bps, stock_code
    ) 
    VALUES(%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"""
    values = [(row['날짜'],row['시가'],row['고가'],row['저가'],row['종가'],
               row['거래량'],row['PER'],row['PBR'],row['EPS'],
               row['BPS'],row['종목코드']) for _, row in datas.iterrows()]
    
    try:
        cursor.executemany(insert_query, values)
        db_connect.commit()
    except Exception as e:
        logger.info(f"데이터 저장 중 오류 발생: {e}")

def save_stock_data_by_basic(datas: List[Dict], db_connect: pymysql.connections.Connection):
    cursor = db_connect.cursor(cursors.DictCursor)

    insert_query = """INSERT INTO stock(code, name, market) VALUES(%s, %s, %s)"""
    delete_query = """DELETE FROM stock WHERE code = %s"""

    values = [(row['종목코드'], row['종목명'], row['구분']) for _, row in datas.iterrows()]
    
    cursor.execute("SELECT code FROM stock")
    existing_codes = {row['code'] for row in cursor.fetchall()}

    new_codes = {row[0] for row in values}
    codes_to_insert = [row for row in values if row[0] not in existing_codes]
    codes_to_delete = existing_codes - new_codes

    try:
        if codes_to_insert:
            cursor.executemany(insert_query, codes_to_insert)

        if codes_to_delete:
            cursor.executemany(delete_query, [(code,) for code in codes_to_delete])

        db_connect.commit()
    except Exception as e:
        logger.info(f"데이터 저장 중 오류 발생: {e}")
        db_connect.rollback()