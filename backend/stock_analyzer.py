import datetime
from pykrx import stock
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class StockAnalyzer:
    TODAY = datetime.datetime.now().strftime('%Y%m%d')
    START_DATE = "19800101"
    JANGTA_DIFF = 5


    @staticmethod
    def is_valid_stock_code(stock_code):
        try:
            stock.get_market_ticker_name(stock_code)
        except Exception as e:
            return False

        return True

    @staticmethod
    def get_valid_stock_name(stock_code):
        try:
            return stock.get_market_ticker_name(stock_code)
        except Exception as e:
            pass

    @staticmethod
    def get_date_n_days_ago(n):
        return (datetime.datetime.now() - datetime.timedelta(days=n)).strftime('%Y%m%d')

    @classmethod
    def fetch_stock_data(cls, stock_codes, date):
        return [
            (stock.get_market_ticker_name(ticker), ticker, ohlcv["거래량"].iloc[0])
            for ticker in stock_codes
            if not (ohlcv := stock.get_market_ohlcv_by_date(date, date, ticker)).empty
        ]

    @staticmethod
    def filter_stocks(stock_data, threshold_volume=100000):
        return [data for data in stock_data if data[2] >= threshold_volume]

    @staticmethod
    def calculate_vwap(df):
        total_value = sum((row['고가'] + row['저가']) * row['거래량'] for index, row in df.iterrows())
        total_volume = df['거래량'].sum()
        return None if not total_volume else total_value / total_volume / 4

    @classmethod
    def analyze_stocks(cls, stock_codes, today):
        data = []
        for stock_code in stock_codes:
            try:
                df = stock.get_market_ohlcv(cls.START_DATE, today, stock_code)
                vwap = cls.calculate_vwap(df)
                if vwap:
                    analyze_result = cls.analyze_stock(df, stock_code, vwap)
                    if analyze_result:
                        print(analyze_result)
                        data.extend(analyze_result)
            except Exception as e:
                pass
        return data

    @classmethod
    def analyze_stock(cls, df, stock_code, vwap):
        data = []
        close = df['종가'].iloc[-1]
        percentage_diff = round(((close - vwap) / vwap) * 100, 2)
        vwap_low, vwap_high = vwap * (1 - (0.01 * cls.JANGTA_DIFF)), vwap * (1 + (0.01 * cls.JANGTA_DIFF))
        if vwap_low <= close <= vwap_high and cls.calculate_equation(df) > 0:
            ticker_name = stock.get_market_ticker_name(stock_code)
            data.append((ticker_name, stock_code, df['거래량'].sum(), percentage_diff, round(vwap)))

        return data

    @staticmethod
    def calculate_equation(df):
        sum_o_less_than_c = sum(row['종가'] * row['거래량'] for index, row in df.iterrows() if row['시가'] < row['종가'])
        sum_o_greater_than_c = sum(row['종가'] * row['거래량'] for index, row in df.iterrows() if row['시가'] > row['종가'])
        return sum_o_less_than_c - sum_o_greater_than_c

    @staticmethod
    def calculate_price_channel(df, period=20):
        df['Upper_Channel'] = df['고가'].rolling(window=period).max()
        df['Lower_Channel'] = df['저가'].rolling(window=period).min()
        return df

    @classmethod
    def is_close_within_range_of_lower_channel(cls, stock_codes):
        data = []
        for stock_code in stock_codes:
            df = stock.get_market_ohlcv(cls.START_DATE, cls.TODAY, stock_code)
            df = cls.calculate_price_channel(df)
            latest_data = df.iloc[-1]

            close_price = latest_data['종가']
            lower_channel = latest_data['Lower_Channel']
            lower_channel_5_percent = lower_channel * 0.07

            is_within_range = (lower_channel - lower_channel_5_percent) <= close_price <= (
                        lower_channel + lower_channel_5_percent)
            percent_difference_from_lower_channel = round(((close_price - lower_channel) / lower_channel) * 100, 2)

            if is_within_range:
                ticker_name = stock.get_market_ticker_name(stock_code)
                data.append((ticker_name, stock_code, latest_data['거래량'].sum(), percent_difference_from_lower_channel))
        return data

    @classmethod
    def draw_candle_chart(cls, stock_code: int):
        thirty_days_before = (datetime.datetime.now() - datetime.timedelta(days=240)).strftime('%Y%m%d')
        df = stock.get_market_ohlcv(thirty_days_before, cls.TODAY, stock_code)

        df['Middle_Band'] = df['종가'].rolling(window=20).mean()
        df['STD'] = df['종가'].rolling(window=20).std()
        df['Upper_Bollinger'] = df['Middle_Band'] + (df['STD'] * 2)
        df['Lower_Bollinger'] = df['Middle_Band'] - (df['STD'] * 2)
        df['Upper_Bound'] = df['고가'].rolling(window=20).max()
        df['Lower_Bound'] = df['저가'].rolling(window=20).min()

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.7, 0.3],
                            vertical_spacing=0.1)

        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['시가'],
                                     high=df['고가'],
                                     low=df['저가'],
                                     close=df['종가'],
                                     name='Candlesticks'), row=1, col=1)

        fig.add_trace(go.Scatter(x=df.index, y=df['Upper_Bollinger'], mode='lines', name='Upper Bollinger',
                                 line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df.index, y=df['Lower_Bollinger'], mode='lines', name='Lower Bollinger',
                                 line=dict(color='green')))
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Middle_Band'], mode='lines', name='Middle Band', line=dict(color='blue')))
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Upper_Bound'], mode='lines', name='Upper Bound', line=dict(color='blue')))
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Lower_Bound'], mode='lines', name='Lower Bound', line=dict(color='blue')))

        colors = df['종가'].diff().apply(lambda x: 'red' if x < 0 else 'green')
        fig.add_trace(go.Bar(x=df.index, y=df['거래량'], name='Volume', marker_color=colors), row=2, col=1)

        fig.update_layout(title=f'Stock {stock_code} Candlestick, Bollinger Bands, Price Channel, and Volume Chart',
                          xaxis_title='Date',
                          yaxis_title='Price (₩)',
                          xaxis_rangeslider_visible=False,
                          template="plotly_dark")

        fig.show()
