import datetime
from pykrx import stock
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class StockAnalyzer:
    TODAY = datetime.datetime.now().strftime('%Y%m%d')
    START_DATE = "19800101"
    JANGTA_DIFF = 5

    @staticmethod
    def get_date_n_days_ago(n):
        """Return the date n days ago in the format YYYYMMDD."""
        date_n_days_ago = (datetime.datetime.now() - datetime.timedelta(days=n)).strftime('%Y%m%d')
        return date_n_days_ago

    @staticmethod
    def get_stock_data_for_date(stock_codes, date):
        """Retrieve stock data for a given date."""
        return [
            (stock.get_market_ticker_name(ticker), ticker, ohlcv["거래량"].iloc[0])
            for ticker in stock_codes
            if (ohlcv := stock.get_market_ohlcv_by_date(date, date, ticker)).empty is False
        ]

    @staticmethod
    def joongta_joongta(stock_codes, date):
        """Retrieve stock data for a given date."""
        return [
            (stock.get_market_ticker_name(ticker), ticker, ohlcv["거래량"].iloc[0])
            for ticker in stock_codes
            if (ohlcv := stock.get_market_ohlcv_by_date(date, date, ticker)).empty is False
        ]

    @staticmethod
    def filter_stocks(stock_data, threshold_volume=100000):
        """Filter stocks based on a volume threshold."""
        return [i for i in stock_data if i[2] >= threshold_volume]

    @staticmethod
    def calculate_vwap(df):
        total_value = sum((row['고가'] + row['저가']) * row['거래량'] for index, row in df.iterrows())
        total_volume = df['거래량'].sum()

        if total_volume:
            return total_value / total_volume / 4
        else:
            return None

    @staticmethod
    def calculate_vwap_with_pykrx(stock_codes):
        data = []
        for stock_code in stock_codes:
            df = stock.get_market_ohlcv(StockAnalyzer.START_DATE, StockAnalyzer.TODAY, stock_code)
            vwap = StockAnalyzer.calculate_vwap(df)

            if vwap:
                close = df['종가'].iloc[-1]

                # Calculate Percentage Difference
                percentage_diff = round(((close - vwap) / vwap) * 100, 2)

                vwap_low, vwap_high = vwap * (1 - (0.01 * StockAnalyzer.JANGTA_DIFF)), vwap * (
                            1 + (0.01 * StockAnalyzer.JANGTA_DIFF))
                if vwap_low <= close <= vwap_high and StockAnalyzer.calculate_equation(df) > 0:
                    print(
                        f"TRUE : Stock Code: {stock_code}, Current price {close} is within the VWAP range ({vwap_low:.2f} <= {vwap:.2f} <= {vwap_high:.2f}). Percentage Difference: {percentage_diff:.2f}%")
                    ticker_name = stock.get_market_ticker_name(stock_code)
                    data.append((ticker_name, stock_code, df['거래량'].sum(), percentage_diff, round(vwap)))
            else:
                print(f"Stock Code: {stock_code}, VWAP calculation is not possible (total volume is 0)")
        return data

    @staticmethod
    def get_joongta_stocks(stock_codes):
        return [StockAnalyzer.get_days_with_high_trading_value(stock) for stock in stock_codes]

    @staticmethod
    def calculate_equation(df):
        # Calculate the sum for days when opening price is less than closing price
        sum_o_less_than_c = sum(row['종가'] * row['거래량'] for index, row in df.iterrows() if row['시가'] < row['종가'])

        # Calculate the sum for days when opening price is greater than closing price
        sum_o_greater_than_c = sum(row['종가'] * row['거래량'] for index, row in df.iterrows() if row['시가'] > row['종가'])

        # Calculate the difference
        result = sum_o_less_than_c - sum_o_greater_than_c

        return result

    @staticmethod
    def calculate_price_channel(df, period=20):
        df['Upper_Channel'] = df['고가'].rolling(window=period).max()
        df['Lower_Channel'] = df['저가'].rolling(window=period).min()
        return df

    @staticmethod
    def get_data_with_price_channel(stock_code):
        period = 20
        df = stock.get_market_ohlcv(StockAnalyzer.START_DATE, StockAnalyzer.TODAY, stock_code)
        return StockAnalyzer.calculate_price_channel(df, period)

    @staticmethod
    def is_close_within_range_of_lower_channel(stock_codes):
        data = []
        for stock_code in stock_codes:
            df = StockAnalyzer.get_data_with_price_channel(stock_code)
            latest_data = df.iloc[-1]

            close_price = latest_data['종가']
            lower_channel = latest_data['Lower_Channel']
            lower_channel_5_percent = lower_channel * 0.07

            is_within_range = (lower_channel - lower_channel_5_percent) <= close_price <= (
                        lower_channel + lower_channel_5_percent)

            # Calculate the percentage difference from the lower channel
            percent_difference_from_lower_channel = ((close_price - lower_channel) / lower_channel) * 100

            # Rounding to 2 decimal places
            percent_difference_from_lower_channel = round(percent_difference_from_lower_channel, 2)

            if is_within_range:
                ticker_name = stock.get_market_ticker_name(stock_code)
                data.append((ticker_name, stock_code, latest_data['거래량'].sum(), percent_difference_from_lower_channel))
        return data

    @staticmethod
    def draw_candle_chart(stock_code: int):
        TODAY = datetime.datetime.now()
        THIRTY_DAYS_BEFORE = TODAY - datetime.timedelta(days=240)
        formatted_30_days_before = THIRTY_DAYS_BEFORE.strftime('%Y%m%d')

        df = stock.get_market_ohlcv(formatted_30_days_before, StockAnalyzer.TODAY, stock_code)

        # Calculate the 20-day simple moving average (Middle Band)
        df['Middle_Band'] = df['종가'].rolling(window=20).mean()

        # Calculate the standard deviation
        df['STD'] = df['종가'].rolling(window=20).std()

        # Calculate the Upper Bollinger Band
        df['Upper_Bollinger'] = df['Middle_Band'] + (df['STD'] * 2)

        # Calculate the Lower Bollinger Band
        df['Lower_Bollinger'] = df['Middle_Band'] - (df['STD'] * 2)

        # Calculate the 20-period price channel
        df['Upper_Bound'] = df['고가'].rolling(window=20).max()
        df['Lower_Bound'] = df['저가'].rolling(window=20).min()

        # Create subplots
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.7, 0.3],  # 70% for candlestick and 30% for volume
                            vertical_spacing=0.1)  # Space between plots

        # Add candlestick trace
        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['시가'],
                                     high=df['고가'],
                                     low=df['저가'],
                                     close=df['종가'],
                                     name='Candlesticks'), row=1, col=1)

        # Add Bollinger Bands traces
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Upper_Bollinger'], mode='lines', name='Upper Bollinger',
                       line=dict(color='red')))
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Lower_Bollinger'], mode='lines', name='Lower Bollinger',
                       line=dict(color='green')))
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Middle_Band'], mode='lines', name='Middle Band', line=dict(color='blue')))

        # Add price channel traces
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Upper_Bound'], mode='lines', name='Upper Bound', line=dict(color='blue')))
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Lower_Bound'], mode='lines', name='Lower Bound', line=dict(color='blue')))

        # Add volume bars trace
        colors = df['종가'].diff().apply(lambda x: 'red' if x < 0 else 'green')
        fig.add_trace(go.Bar(x=df.index, y=df['거래량'], name='Volume', marker_color=colors), row=2, col=1)

        fig.update_layout(title=f'Stock {stock_code} Candlestick, Bollinger Bands, Price Channel, and Volume Chart',
                          xaxis_title='Date',
                          yaxis_title='Price (₩)',
                          xaxis_rangeslider_visible=False,
                          template="plotly_dark")

        fig.show()


