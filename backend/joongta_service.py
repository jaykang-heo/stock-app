import datetime
from pykrx import stock
import plotly.graph_objects as go
from plotly.subplots import make_subplots

TODAY = datetime.datetime.now().strftime('%Y%m%d')
START_DATE = "19800101"
B_values = []  # List to store values of B for each date


@staticmethod
def calculate_B(df):
    """
    Calculate the value of B using the equation:
    B = sum(if(o<c,c*v,0))-sum(if(o>c,c*v,0))
    """
    # Calculate the sum for days when opening price is less than closing price
    sum_o_less_than_c = sum(row['종가'] * row['거래량'] for index, row in df.iterrows() if row['시가'] < row['종가'])

    # Calculate the sum for days when opening price is greater than closing price
    sum_o_greater_than_c = sum(row['종가'] * row['거래량'] for index, row in df.iterrows() if row['시가'] > row['종가'])

    # Calculate the difference
    B = sum_o_less_than_c - sum_o_greater_than_c

    return B



@staticmethod
def calculate_B2(df):
    """
    Calculate the value of B2 using the equation:
    B2 = valueWhen(1, date(1)!=date, B(1))
    """
    # Since the date column in df is the index
    current_date = df.index[-1]
    previous_date = df.index[-2]

    # If the current date is not the same as the previous date, then B2 should be the previous value of B.
    if current_date != previous_date and B_values:
        B2 = B_values[-1]  # Get the previous value of B
    else:
        B2 = 0  # Default value

    return B2


@staticmethod
def check_equation(df, stock_code):
    """
    Check if the difference between B and B2 is greater than 10,000,000,000.
    If the condition is satisfied, return the stock name, ticker, and volume.
    """
    B = calculate_B(df)
    B_values.append(B)  # Update the B_values list with the current value of B
    B2 = calculate_B2(df)
    # 1310012822947
    if B > 10000000000:
        ticker_name = stock.get_market_ticker_name(stock_code)
        last_day_volume = df['거래량'].iloc[-1]  # Extracting the volume of the last row
        return ticker_name, stock_code, last_day_volume
    else:
        pass


def calculat_joongta(stock_codes):
    res = []
    for stock_code in stock_codes:
        # df = stock.get_market_ohlcv_by_date(START_DATE, TODAY, stock_code)
        df = stock.get_market_trading_value_by_date(START_DATE, TODAY, stock_code)

        # Get the '거래대금' value for the given stock code
        print(stock_code, df)
        trade_value = df.loc[int(stock_code), '전체']
        if (trade_value > 10000000000):
            ticker_name = stock.get_market_ticker_name(stock_code)
            last_day_volume = df['거래량'].iloc[-1]  # Extracting the volume of the last row
            res.append((ticker_name, stock_code, last_day_volume))

        # data = str(check_equation(trade_value, stock_code))
        # res.append(data)
    print(res)
    return res
