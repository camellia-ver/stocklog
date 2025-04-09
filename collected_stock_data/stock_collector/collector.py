from .price_fetcher import get_current_price
from .utils import now_str, load_or_create_name_dict
from .db import connect_db, save_stock_data_by_realtime, save_stock_data_by_daily
from .logger import logger
import pandas as pd
from datetime import datetime
import os, time, random
from pykrx import stock

def create_stock_data_by_realtime(codes:dict, duration_minutes:int):
    name_dict = load_or_create_name_dict()
    all_data = []

    for i in range(duration_minutes): 
        next_time = datetime.now()
        logger.info(f"\n========== {i+1}/{duration_minutes}분 수집 시작 ==========")

        now = now_str()
        logger.info(f"\n[{now}] 수집시작")

        minute_data = []
        for category, code_list in codes.items():
            for code in code_list:
                price = get_current_price(code)
                if price is not None:
                    minute_data.append({
                        "시간": now_str(),
                        "종목코드":code,
                        "종목명": name_dict.get(code, "Unknown"),   
                        "현재가":price,
                        "구분":category
                    })
                    logger.info(f"[{now}] {code} - {name_dict.get(code, 'Unknown')} : {price}원")
                time.sleep(random.uniform(1.0,2.5))

        all_data.extend(minute_data)
        logger.info(f"[{now}] 수집완료: {len(minute_data)} 종목")

        next_time = next_time + pd.Timedelta(minutes=1)
        sleep_duration = (next_time - datetime.now()).total_seconds()
        if sleep_duration > 0:
            time.sleep(sleep_duration)
        else:
            logger.info("⚠️ 수집 시간이 1분을 초과했습니다.")
    
    all_data_df = pd.DataFrame(all_data)
    now_filename = now_str('%Y-%m-%d_%H-%M-%S')
    all_data_df.to_csv(f"data/prices/stock_price_{now_filename}.csv", index=False, encoding='utf-8-sig')

    db_connect = connect_db()
    if db_connect:
        save_stock_data_by_realtime(all_data, db_connect)
        db_connect.close()

def get_stock_data(date: str, code: str) -> pd.DataFrame:
    ohlcv = stock.get_market_ohlcv_by_date(date,date,code)
    fundamental = stock.get_market_fundamental_by_date(date,date,code)

    return pd.concat([ohlcv, fundamental], axis=1)

def create_stock_data_by_daily(codes:dict, date: str):
    name_dict = load_or_create_name_dict()
    all_data = []

    for category, code_list in codes.items():
        for code in code_list:
            try:
                logger.info(f"[{category}] 진행중중 {code} - {name_dict.get(code, 'Unknown')}")
                
                merged = get_stock_data(date, code)  
                merged.reset_index(inplace=True)
                merged['구분'] = category
                merged['종목명'] = name_dict.get(code, "Unknown")
                merged['종목코드'] = code

                all_data.append(merged)
            except Exception as e:
                logger.info(f"{code}({name_dict.get(code, 'Unknown')})에서 오류 발생: {e}")

    if all_data:
        result_df = pd.concat(all_data)
        result_df.to_csv(f"data/summary/market_data_{date}.csv", encoding='utf-8-sig', index=False)
        logger.info(f"{len(result_df)}개 저장")

    db_connect = connect_db()
    if db_connect:
        save_stock_data_by_daily(all_data, db_connect)
        db_connect.close()