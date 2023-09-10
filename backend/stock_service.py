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


def calculate_vwap_with_pykrx(stock_codes):
    data = []
    start_date = "19800101"
    for stock_code in stock_codes:
        df = stock.get_market_ohlcv(start_date, get_date_n_days_ago(0), stock_code)

        total_value = 0
        total_volume = 0

        for index, row in df.iterrows():
            high = row['고가']
            low = row['저가']
            close = row['종가']
            volume = row['거래량']

            total_value += (high + low) * volume
            total_volume += volume

        if total_volume != 0:
            vwap = total_value / total_volume / 4
            vwap_low = vwap * 0.95
            vwap_high = vwap * 1.05

            if vwap_low <= close <= vwap_high:
                print(f"TRUE : Stock Code: {stock_code}, Current price {close} is within the VWAP range ({vwap_low:.2f} <= {vwap:.2f} <= {vwap_high:.2f})")
                ticker_name = stock.get_market_ticker_name(stock_code)
                data.append((ticker_name, stock_code, total_volume))
            else:
                # print(
                #     f"FALSE : Stock Code: {stock_code}, Current price {close} is not within the VWAP range ({vwap_low:.2f} <= {vwap:.2f} <= {vwap_high:.2f})")
                pass
        else:
            print(f"Stock Code: {stock_code}, VWAP calculation is not possible (total volume is 0)")
    return data

