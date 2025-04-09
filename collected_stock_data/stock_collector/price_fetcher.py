import requests, random
from bs4 import BeautifulSoup
from .errors import write_error_code
from .utils import now_str
from concurrent.futures import ThreadPoolExecutor, as_completed
from .logger import logger

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 Chrome/91.0.4472.77 Mobile Safari/537.36"
]
        
def get_current_price(code:str) -> int:
    try:
        
        url = f"https://finance.naver.com/item/main.naver?code={code}"
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
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
        logger.info(f"[{code}] 요청 오류 발생: {e}")
        write_error_code(code)
    except Exception as e:
        logger.info(f"[{code}]에서 문제 발생: {e}")
        write_error_code(code)

    return None

  