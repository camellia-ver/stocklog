import multiprocessing
from stock_collector.utils import init_env, now_str
from worker import process_stock_data

if __name__ == '__main__':
    init_env()

    today = now_str('%Y-%m-%d')
    code_groups = ['KOSPI','KOSDAQ']
    
    process_count = min(len(code_groups), multiprocessing.cpu_count)
    with multiprocessing.Pool(process_count) as pool:
        pool.map(process_stock_data, code_groups)