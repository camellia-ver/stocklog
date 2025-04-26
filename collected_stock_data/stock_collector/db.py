import pymysql
from pymysql import cursors
from dotenv import load_dotenv
from pandas import DataFrame
import os
from .logger import logger

load_dotenv()

def get_db_connection() -> pymysql.connections.Connection:
    """
    .env 환경변수를 기반으로 MySQL 데이터베이스에 연결합니다.

    Returns:
        pymysql.connections.Connection: 데이터베이스 연결 객체

    Raises:
        pymysql.MySQLError: 연결 실패 시 예외 발생
    """
    try:
        connection = pymysql.connect(
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            db=os.getenv("DB_NAME"),
            charset='utf8'
        )

        return connection
    except pymysql.MySQLError as e:
        logger.error("DB 연결 실패", exc_info=True)
        raise pymysql.MySQLError("DB 연결에 실패했습니다.") from e

def save_daily_stock_data(stock_data: DataFrame, connection: pymysql.connections.Connection):
    """
    일별 주가 데이터를 dailysummarystock 테이블에 저장합니다.

    Args:
        stock_data (DataFrame): '날짜', '시가', '고가', '저가', '종가', '거래량', 'PER', 'PBR', 'EPS', 'BPS', '종목코드' 컬럼을 가진 데이터프레임
        connection (pymysql.connections.Connection): 데이터베이스 연결 객체

    Raises:
        Exception: 데이터 저장 중 오류 발생 시 로그를 출력하고 롤백
    """
    db_cursor = connection.cursor(cursors.DictCursor)

    insert_sql = """INSERT INTO dailysummarystock(
        date, open_price, high_price, low_price, close_price, 
        volume, per, pbr, eps, bps, stock_code
    ) 
    VALUES(%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"""
    insert_values = [(row['날짜'], row['시가'], row['고가'], row['저가'], row['종가'],
               row['거래량'], row['PER'], row['PBR'], row['EPS'],
               row['BPS'], row['종목코드']) for _, row in stock_data.iterrows()]

    try:
        batch_size = 1000
        for i in range(0, len(insert_values), batch_size):
            db_cursor.executemany(insert_sql, insert_values[i:i+batch_size])
        connection.commit()
    except pymysql.IntegrityError as e:
        if e.args[0] == 1062: 
            logger.warning(f"중복된 값이 존재하여 삽입되지 않았습니다: {e}")
            connection.rollback()  
        else:
            logger.error("데이터 저장 중 오류 발생", exc_info=True)
            connection.rollback()
    except Exception as e:
        logger.error("예기치 못한 오류 발생", exc_info=True)
        connection.rollback()
    finally:
        close_connection(connection)

def fetch_existing_stock_codes(connection: pymysql.connections.Connection) -> set:
    """
    stock 테이블에서 현재 존재하는 종목 코드를 조회합니다.

    Args:
        connection (pymysql.connections.Connection): 데이터베이스 연결 객체

    Returns:
        set: 기존에 존재하는 종목 코드들의 집합
    """
    db_cursor = connection.cursor(cursors.DictCursor)
    db_cursor.execute("SELECT code FROM stock")
    return {row['code'] for row in db_cursor.fetchall()}

def save_basic_stock_data(datas: DataFrame, connection: pymysql.connections.Connection):
    """
    주식 종목 기본 정보를 stock 테이블에 저장합니다.
    기존에 존재하지 않는 종목은 삽입하고, 더 이상 존재하지 않는 종목은 삭제합니다.

    Args:
        datas (DataFrame): '종목코드', '종목명', '구분' 컬럼을 가진 데이터프레임
        connection (pymysql.connections.Connection): 데이터베이스 연결 객체

    Raises:
        Exception: 삽입 또는 삭제 중 오류 발생 시 로그를 출력하고 롤백
    """
    db_cursor = connection.cursor(cursors.DictCursor)

    insert_query = """INSERT INTO stock(code, name, market) VALUES(%s, %s, %s)"""
    delete_query = """DELETE FROM stock WHERE code = %s"""

    values = [(row['종목코드'], row['종목명'], row['구분']) for _, row in datas.iterrows()]

    existing_codes = fetch_existing_stock_codes(connection)

    new_codes = {row[0] for row in values}
    codes_to_insert = [row for row in values if row[0] not in existing_codes]
    codes_to_delete = existing_codes - new_codes

    try:
        if codes_to_insert:
            db_cursor.executemany(insert_query, codes_to_insert)

        if codes_to_delete:
            db_cursor.executemany(delete_query, [(code,) for code in codes_to_delete])

        connection.commit()
    except Exception as e:
        logger.error("데이터 저장 중 오류 발생", exc_info=True)
        connection.rollback()
    finally:
        close_connection(connection)

def fetch_stock_codes_by_market(market: str) -> set:
    """
    지정한 시장(market)에 해당하는 종목 코드들을 데이터베이스에서 조회합니다.

    Args:
        market (str): 시장 구분 (예: 'KOSPI', 'KOSDAQ')

    Returns:
        set: 해당 시장의 종목 코드 집합
    """
    connection = None
    try:
        connection = get_db_connection()
        db_cursor = connection.cursor(cursors.DictCursor)

        db_cursor.execute("SELECT code FROM stock WHERE market = %s", (market,))
        codes = {row['code'] for row in db_cursor.fetchall()}

        return codes
    except Exception as e:
        logger.error("주식 코드 조회 중 오류 발생", exc_info=True)
        return set()
    finally:
        close_connection(connection)

def close_connection(connection: pymysql.connections.Connection):
    """
    데이터베이스 연결을 종료합니다.

    Args:
        connection (pymysql.connections.Connection): 종료할 데이터베이스 연결 객체
    """
    connection.close()  