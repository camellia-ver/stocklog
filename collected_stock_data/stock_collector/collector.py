from .utils import now_str, save_to_csv, save_to_db
from .logger import logger
import pandas as pd
from datetime import datetime
from pykrx import stock
from typing import List,Set

def collect_daily_stock_data(codes: Set[str], start_date:str, end_date:str) -> None:
    """
    종목 코드 리스트와 날짜 범위를 기반으로 일간 주식 데이터를 수집하고 CSV 및 DB에 저장합니다.

    Args:
        codes (Set[str]): 종목 코드 리스트.
        start_date (str): 데이터 수집 시작일자 (형식: 'YYYYMMDD').
        end_date (str): 데이터 수집 종료일자 (형식: 'YYYYMMDD').

    Returns:
        None
    """
    collected_dataframes = []

    for code in codes:
        try:
            logger.info(f"[collect_daily_stock_data] {code} 처리 시작")
                
            merged_stock_data = get_daily_summary_stock_data(start_date, end_date, code)  
            merged_stock_data = add_code_and_reset_index(merged_stock_data, code)

            collected_dataframes.append(merged_stock_data)
        except Exception as e:
            logger.error(f"[collect_daily_stock_data] {code} 처리 중 오류 발생: {e}")
    
    if collected_dataframes:
        final_result_df = pd.concat(collected_dataframes, ignore_index=True)
        save_to_csv(final_result_df,now_str('%Y_%m_%d'),"daily")
        save_to_db(final_result_df, "daily")
    else:
        logger.warning("수집된 데이터가 없습니다.")

def add_code_and_reset_index(df: pd.DataFrame, code:str) -> pd.DataFrame:
    """
    데이터프레임의 인덱스를 초기화하고 종목코드 컬럼을 추가합니다.

    Args:
        df (pd.DataFrame): 종목별 일간 데이터프레임.
        code (str): 종목 코드.

    Returns:
        pd.DataFrame: 인덱스가 초기화되고 '종목코드' 컬럼이 추가된 데이터프레임.
    """
    df.reset_index(inplace=True)
    df['종목코드'] = code
    return df

def collect_basic_stock_info():
    """
    오늘 날짜 기준으로 KOSPI 및 KOSDAQ 종목 기본 정보를 수집하여 CSV 및 DB에 저장합니다.

    Returns:
        None
    """
    basic_stock_df = get_stock_basic_data()
    
    save_to_csv(basic_stock_df, now_str('%Y_%m_%d'), "basic")
    save_to_db(basic_stock_df, "basic")

def get_stock_codes_by_date(date_str: str, market: str) -> List[str]:
    """
    지정된 날짜와 시장(KOSPI 또는 KOSDAQ)에서 종목 코드 리스트를 반환합니다.
    
    Parameters:
        date_str (str): 조회 기준 날짜 (예: '20240418')
        market (str): 'KOSPI' 또는 'KOSDAQ'

    Returns:
        List[str]: 종목 코드 리스트
    """
    try:
        return stock.get_market_ticker_list(date_str, market=market)
    except Exception as e:
        logger.error(f"[get_stock_codes_by_date] 오류 발생: {e}")
        return []

def get_daily_summary_stock_data(start_data: str,end_date: str,code: str) -> pd.DataFrame:
    """
    특정 종목 코드에 대해 OHLCV 및 재무지표 데이터를 수집하여 병합된 데이터프레임을 반환합니다.

    Args:
        start_date (str): 수집 시작일 (형식: 'YYYYMMDD').
        end_date (str): 수집 종료일 (형식: 'YYYYMMDD').
        code (str): 종목 코드.

    Returns:
        pd.DataFrame: 수집된 데이터프레임. 수집 실패 시 빈 데이터프레임 반환.
    """
    try:
        ohlcv = stock.get_market_ohlcv_by_date(start_data,end_date,code)
        fundamental = stock.get_market_fundamental_by_date(start_data,end_date,code)

        if ohlcv.empty:
            logger.warning(f"[get_daily_summary_stock_data] OHLCV 데이터 없음: {code} - {start_data}~{end_date}")
        if fundamental.empty:
            logger.warning(f"[get_daily_summary_stock_data] 재무 데이터 없음: {code} - {start_data}~{end_date}")
        if ohlcv.empty or fundamental.empty:
            return pd.DataFrame()

        logger.info(f"[get_daily_summary_stock_data] 데이터 수집 성공: {code} - {start_data}~{end_date}")
        return pd.concat([ohlcv, fundamental], axis=1, join='inner')  
    except Exception as e:
        logger.error(f"[get_daily_summary_stock_data] 오류 발생: {code} - {e}")
        return pd.DataFrame()

def get_stock_basic_data(date_str=None) -> pd.DataFrame:
    """
    기준 일자의 전체 종목 코드, 종목명, 시장구분(KOSPI/KOSDAQ)을 수집하여 반환합니다.

    Args:
        date_str (str, optional): 기준 일자 (형식: 'YYYYMMDD'). None이면 오늘 날짜 기준.

    Returns:
        pd.DataFrame: 종목 기본 정보 데이터프레임. 수집 실패 시 빈 DataFrame 반환.
    """
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
    
    return pd.DataFrame(stock_list)