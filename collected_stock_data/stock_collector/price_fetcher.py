import requests, random, time
from bs4 import BeautifulSoup
from .error_handler import write_error_code
from concurrent.futures import ThreadPoolExecutor, as_completed
from .logger import logger
from typing import Optional    

def get_current_price(code:str, max_retries:int=3, retry_delay:float=1.5) -> Optional[int]:
    url = f"https://finance.daum.net/api/quotes/A{code}?summary=false"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G975N) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        "Referer": f"https://finance.daum.net/quotes/A{code}"
    }   
    
    for attempt in range(1, max_retries+1):
        try:         
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            data = res.json()

            price = data.get("tradePrice")
            if price is not None:
                # 가격은 정수 단위로 반환 (ex. 14250원)
                return int(price)
            else:
                logger.warning(f"[{code}] 응답에 'tradePrice' 없음: {data}")
                return None
        except requests.RequestException as e:
            logger.error(f"[{code}]에서 문제 발생: {e}")
        except Exception as e:
            logger.error(f"[{code}]에서 문제 발생 (시도 {attempt}/{max_retries}): {e}")

        if attempt < max_retries:
            time.sleep(retry_delay)

    write_error_code(code)
    return None

def get_multiple_prices(codes: list[str], max_workers: int = 10) -> dict[str, int]:
    result = {}
    codes = list(map(str, codes))

    with ThreadPoolExecutor(max_workers) as executor:
        future_to_code = {
            executor.submit(get_current_price, code): code for code in codes
            }

        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                price = future.result()
                if price is not None:
                    result[code] = price
            except Exception as e:
                logger.error(f"[{code}] 병렬 처리 중 예외 발생: {e}")

        if not result:
            logger.warning("❌ 모든 종목 가격 수집 실패")

        return result
