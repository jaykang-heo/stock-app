# import csv
# import datetime
# from pykrx import stock
#
# TODAY = datetime.datetime.now().strftime('%Y%m%d')
# START_DATE = "19800101"
#
#
# def get_date_n_days_ago(n):
#     """Return the date n days ago in the format YYYYMMDD."""
#     date_n_days_ago = (datetime.datetime.now() - datetime.timedelta(days=n)).strftime('%Y%m%d')
#     return date_n_days_ago
#
#
# def get_stock_codes_from_csv(csv_path):
#     """Extract stock codes from a CSV file."""
#     with open(csv_path, 'r', encoding='utf-8-sig') as file:
#         reader = csv.DictReader(file)
#         return [row['코드번호'][1:] for row in reader]  # Remove 'A' and return list directly
#
#
# def get_stock_data_for_date(stock_codes, date):
#     """Retrieve stock data for a given date."""
#     return [
#         (stock.get_market_ticker_name(ticker), ticker, ohlcv["거래량"].iloc[0])
#         for ticker in stock_codes
#         if (ohlcv := stock.get_market_ohlcv_by_date(date, date, ticker)).empty is False
#     ]
#
#
# def filter_stocks(stock_data, threshold_volume=100000):
#     """Filter stocks based on a volume threshold."""
#     return [i for i in stock_data if i[2] >= threshold_volume]
#
#
# def calculate_vwap(df):
#     total_value = sum((row['고가'] + row['저가']) * row['거래량'] for index, row in df.iterrows())
#     total_volume = df['거래량'].sum()
#
#     if total_volume:
#         return total_value / total_volume / 4
#     else:
#         return None
#
#
# def calculate_vwap_with_pykrx(stock_codes):
#     data = []
#     for stock_code in stock_codes:
#         df = stock.get_market_ohlcv(START_DATE, TODAY, stock_code)
#         vwap = calculate_vwap(df)
#
#         if vwap:
#             close = df['종가'].iloc[-1]
#             vwap_low, vwap_high = vwap * 0.95, vwap * 1.05
#             if vwap_low <= close <= vwap_high:
#                 print(f"TRUE : Stock Code: {stock_code}, Current price {close} is within the VWAP range ({vwap_low:.2f} <= {vwap:.2f} <= {vwap_high:.2f})")
#                 ticker_name = stock.get_market_ticker_name(stock_code)
#                 data.append((ticker_name, stock_code, df['거래량'].sum()))
#         else:
#             print(f"Stock Code: {stock_code}, VWAP calculation is not possible (total volume is 0)")
#     return data
