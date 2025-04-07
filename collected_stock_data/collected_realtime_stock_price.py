import requests
from bs4 import BeautifulSoup
from pykrx import stock
from datetime import datetime
import time
import pandas as pd
import json
import os
import pymysql
from pymysql import cursors
from dotenv import load_dotenv
from typing import List,Dict

def get_current_price(code:str) -> int:
    try:
        url = f"https://finance.naver.com/item/main.naver?code={code}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.select_one("#chart_area div.rate_info div.today p.no_today span.blind")
        
        if price_tag and price_tag.text:
            return int(price_tag.text.replace(",", ""))
        else:
            raise ValueError("가격 정보 태그를 찾을 수 없음.")
    except requests.exceptions.RequestException as e:
        print(f"[{code}] 요청 오류 발생: {e}")
        write_error_code(code)
    except Exception as e:
        print(f"[{code}]에서 문제 발생: {e}")
        write_error_code(code)

    return None

def write_error_code(code:str,base_path="data/logs"):
    date_str = now_str('%Y-%m-%d')
    filepath = os.path.join(base_path, f"get_price_function_error_codes_{date_str}.txt")
    with open(filepath,'a', encoding="utf-8") as f:
        f.write(f"{code}\n")

def create_stock_data(codes:dict, duration_minutes:int):
    name_dict = load_or_create_name_dict()
    all_data = []

    for i in range(duration_minutes): 
        next_time = datetime.now()
        print(f"\n========== {i+1}/{duration_minutes}분 수집 시작 ==========")

        now = now_str("%Y-%m-%d %H:%M:%S")
        print(f"\n[{now}] 수집시작")

        minute_data = []
        for category, code_list in codes.items():
            for code in code_list:
                price = get_current_price(code)
                if price is not None:
                    minute_data.append({
                        "시간":now,
                        "종목코드":code,
                        "종목명": name_dict.get(code, "Unknown"),   
                        "현재가":price,
                        "구분":category
                    })
                    print(f"[{now}] {code} - {name_dict.get(code, 'Unknown')} : {price}원")
                time.sleep(0.1)

        all_data.extend(minute_data)
        print(f"[{now}] 수집완료: {len(minute_data)} 종목")

        next_time = next_time + pd.Timedelta(minutes=1)
        sleep_duration = (next_time - datetime.now()).total_seconds()
        if sleep_duration > 0:
            time.sleep(sleep_duration)
        else:
            print("⚠️ 수집 시간이 1분을 초과했습니다.")
    
    all_data_df = pd.DataFrame(all_data)
    now_str = now_str('%Y-%m-%d_%H-%M-%S')
    all_data_df.to_csv(f"data/prices/stock_price_{now_str}.csv", index=False, encoding='utf-8-sig')

    db_connect = connect_db()
    if db_connect:
        save_stock_data(all_data, db_connect)
        db_connect.close()

def load_or_create_name_dict(filepath="data/name_dict.json") -> dict:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding="utf-8") as f:
            return json.load(f)
        
    name_dict = get_name_dict()
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(name_dict, f, ensure_ascii=False, indent=2)

    return name_dict

def get_name_dict():
    name_dict = {}

    for market in ("KOSPI","KOSDAQ"):
        codes = stock.get_market_ticker_list(datetime.today().strftime('%Y%m%d'), market=market)
        for code in codes:
            name_dict[code] = stock.get_market_ticker_name(code)
            time.sleep(0.1)
    
    return name_dict

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
        print(f"DB 연결 실패: {e}")
        return None

def save_stock_data(datas: List[Dict], db_connect: pymysql.connections.Connection):
    cursor = db_connect.cursor(cursors.DictCursor)

    insert_query = """INSERT INTO stock(code, name, price, time, market) VALUES(%s, %s, %s, %s, %s)"""
    values = [(data['종목코드'],data['종목명'],data['현재가'],data['시간'],data['구분']) for data in datas]
    cursor.executemany(insert_query, values)

    db_connect.commit()

def now_str(fmt='%Y-%m-%d %H:%M:%S') -> str:
    return datetime.now().strftime(fmt)

if __name__ == '__main__':
    os.makedirs("data/logs", exist_ok=True)
    os.makedirs("data/prices", exist_ok=True)

    kospi_codes = stock.get_market_ticker_list(datetime.today().strftime('%Y%m%d'), market="KOSPI")
    kosdaq_codes = stock.get_market_ticker_list(datetime.today().strftime('%Y%m%d'), market="KOSDAQ")

    codes_dict = {
        "KOSPI" : kospi_codes,
        "KOSDAQ" : kosdaq_codes
    }
    duration_minutes = 2 #60 * 24 # 실행하고 싶은 시간(단위:분)

    create_stock_data(codes_dict,duration_minutes)