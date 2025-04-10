import requests, random, time
from bs4 import BeautifulSoup
from .error_handler import write_error_code, read_error_codes
from concurrent.futures import ThreadPoolExecutor, as_completed
from .logger import logger
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 Chrome/91.0.4472.77 Mobile Safari/537.36"
]
        
def get_current_price(code:str, max_retries:int=3, retry_delay:float=1.5) -> Optional[int]:
    for attempt in range(1, max_retries+1):
        try:
            url = f"https://finance.naver.com/item/main.naver?code={code}"
            headers = {
                "User-Agent": random.choice(USER_AGENTS)
            }
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
        
            soup = BeautifulSoup(response.text, "html.parser")
            # price_tag = soup.select_one("#chart_area div.rate_info div.today p.no_today span.blind")
            price_tag = soup.select_one(".rate_info .no_today .blind")

            if price_tag and price_tag.text:
                return int(price_tag.text.replace(",", ""))
            else:
                raise ValueError("가격 정보 태그를 찾을 수 없음.")
        except requests.exceptions.RequestException as e:
            logger.warning(f"[{code}] 요청 오류 발생: {e}")
        except Exception as e:
            logger.er(f"[{code}]에서 문제 발생: {e}")

        if attempt < max_retries:
            time.sleep(retry_delay)

    write_error_code(code)
    return None

def get_multiple_prices(codes: list[str]) -> dict[str, int]:
    result = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_code = {executor.submit(get_current_price, code): code for code in codes}

        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                price = future.result()
                if price is not None:
                    result[code] = price
            except Exception as e:
                logger.error(f"[{code}] 병렬 처리 중 예외 발생: {e}")

        return result
