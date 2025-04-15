from stock_collector.collector import create_stock_data_by_daily, get_codes
from stock_collector.utils import now_str

def process_stock_data(code_group: str):
    today = now_str('%Y-%m-%d')
    codes = get_codes(today, code_group)
    create_stock_data_by_daily(codes, today)
