from stock_collector.utils import init_env
from stock_collector.multiprocessing import run_parallel_collection

if __name__ == '__main__':  
    init_env()

    code_groups = ['KOSPI','KOSDAQ']
    start_data = '20250425'
    end_date = '20250425'
    
    run_parallel_collection(code_groups, start_data, end_date)