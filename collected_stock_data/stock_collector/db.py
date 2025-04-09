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

def save_stock_data_by_realtime(datas: List[Dict], db_connect: pymysql.connections.Connection):
    cursor = db_connect.cursor(cursors.DictCursor)

    insert_query = """INSERT INTO stock(code, name, price, created_at, market) VALUES(%s, %s, %s, %s, %s)"""
    values = [(data['종목코드'],data['종목명'],data['현재가'],data['시간'],data['구분']) for data in datas]
    
    try:
        cursor.executemany(insert_query, values)
        db_connect.commit()
    except Exception as e:
        logger.info(f"데이터 저장 중 오류 발생: {e}")

def save_stock_data_by_daily(datas: List[Dict], db_connect: pymysql.connections.Connection):
    cursor = db_connect.cursor(cursors.DictCursor)

    insert_query = """INSERT INTO stock(
        code, name, date, 
        open_price, high_price, low_price, close_price, 
        volume, per, pbr, eps, bps, market
    ) 
    VALUES(%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"""
    values = [(data['종목코드'],data['종목명'],data['날짜'],
               data['시가'],data['고가'],data['저가'],data['종가'],
               data['거래량'],data['PER'],data['PBR'],data['EPS'],
               data['BPS'],data['구분']) for data in datas]
    
    try:
        cursor.executemany(insert_query, values)
        db_connect.commit()
    except Exception as e:
        logger.info(f"데이터 저장 중 오류 발생: {e}")
