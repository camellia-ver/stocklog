from .utils import now_str, save_to_csv, save_to_db
from .logger import logger
import pandas as pd
from datetime import datetime
from pykrx import stock

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

def get_codes(date_str: str, market: str) -> list:
    try:
        return stock.get_market_ticker_list(date_str, market=market)
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