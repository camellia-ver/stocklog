import os
from .utils import now_str

def write_error_code(code:str,base_path="data/logs"):
    os.makedirs(base_path, exist_ok=True)
    date_str = now_str('%Y-%m-%d')
    filepath = os.path.join(base_path, f"get_price_function_error_codes_{date_str}.txt")
    with open(filepath,'a', encoding="utf-8") as f:
        f.write(f"{code}\n")
