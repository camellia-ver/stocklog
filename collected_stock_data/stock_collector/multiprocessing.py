from .db import fetch_stock_codes_by_market
from .collector import collect_daily_stock_data
from concurrent.futures import ThreadPoolExecutor

def process_market_group(market_types:set, start_date:str, end_date:str) -> None:
    """
    주어진 시장 구분 코드에 해당하는 종목들을 조회하고, 
    해당 종목들의 일별 주가 데이터를 수집합니다.

    Args:
        market_types (set): 시장 구분 코드 집합 (예: {"KOSPI", "KOSDAQ"})
        start_date (str): 수집 시작일 (형식: 'YYYY-MM-DD')
        end_date (str): 수집 종료일 (형식: 'YYYY-MM-DD')
    """
    stock_codes = fetch_stock_codes_by_market(market_types)
    collect_daily_stock_data(stock_codes, start_date, end_date)

def run_parallel_collection(market_groups, start_date, end_date) -> None:
    """
    코드 그룹별로 주가 데이터를 병렬로 수집합니다.

    Args:
        market_groups (Iterable[set]): 각 작업 단위로 처리할 시장 코드 그룹 리스트
        start_date (str): 수집 시작일 (형식: 'YYYY-MM-DD')
        end_date (str): 수집 종료일 (형식: 'YYYY-MM-DD')

    Notes:
        ThreadPoolExecutor를 사용하여 병렬로 데이터를 수집합니다.
    """
    with ThreadPoolExecutor() as executor:
        executor.map(lambda group: process_market_group(group, start_date, end_date), market_groups)