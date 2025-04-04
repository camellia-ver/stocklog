import requests
from bs4 import BeautifulSoup
from pykrx import stock
from datetime import datetime
import time
import pandas as pd

def get_current_price(code):
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
            print(f"[{code}] 가격 정보 태그를 찾을 수 없음.")
    except requests.exceptions.RequestException as e:
        print(f"[{code}] 요청 오류 발생: {e}")
    except Exception as e:
        print(f"[{code}]에서 문제 발생: {e}")
    return None

tickers = stock.get_market_ticker_list(datetime.today().strftime('%Y%m%d'), market="ALL")
name_dict = {code:stock.get_market_ticker_name(code) for code in tickers}

all_data = []
duration_minutes = 2 #60 * 24 # 실행하고 싶은 시간(단위:분)
for i in range(duration_minutes): 
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now}] 수집시작")

    minute_data = []
    for code in tickers:
        price = get_current_price(code)
        if price is not None:
            minute_data.append({
                "시간":now,
                "종목코드":code,
                "종목명":name_dict[code],   
                "현재가":price
            })
            print(f"[{now}] {code} - {name_dict[code]} : {price}원")
        time.sleep(0.1)

    all_data.extend(minute_data)
    print(f"[{now}] 수집완료: {len(minute_data)} 종목")

    minute_df = pd.DataFrame(minute_data)
    minute_df.to_csv(f"stock_price_{now.replace(':','-')}.csv", index=False, encoding='utf-8-sig')

    time.sleep(60)

