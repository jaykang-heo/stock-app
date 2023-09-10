import csv
import datetime
from pykrx import stock

def get_date_n_days_ago(n):
    """Return the date n days ago in the format YYYYMMDD."""
    date_n_days_ago = datetime.datetime.now() - datetime.timedelta(days=n)
    return date_n_days_ago.strftime('%Y%m%d')


def get_stock_codes_from_csv(csv_path):
    """Extract stock codes from a CSV file."""
    stock_codes = []
    with open(csv_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stock_code_with_A = row['코드번호']
            stock_code = stock_code_with_A[1:]  # Remove 'A'
            stock_codes.append(stock_code)
    return stock_codes


def get_stock_data_for_date(stock_codes, date):
    """Retrieve stock data for a given date."""
    stock_data = []
    for ticker in stock_codes:
        ohlcv = stock.get_market_ohlcv_by_date(date, date, ticker)
        ticker_name = stock.get_market_ticker_name(ticker)

        try:
            volume = ohlcv["거래량"].iloc[0]
            stock_data.append((ticker_name, ticker, volume))
        except Exception:
            pass
    return stock_data


def filter_stocks(stock_data, threshold_volume=100000):
    """Filter stocks based on a volume threshold."""
    return [i for i in stock_data if i[2] >= threshold_volume]
