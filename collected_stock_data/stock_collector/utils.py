from datetime import datetime
import json, os, time
from pykrx import stock

def now_str(fmt='%Y-%m-%d %H:%M:%S') -> str:
    return datetime.now().strftime(fmt)

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
    
    return name_dict