from pykrx.stock import get_market_ohlcv_by_ticker
from datetime import datetime, timedelta

yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
df = get_market_ohlcv_by_ticker(date=yesterday, market="ALL")