from fastapi import APIRouter, Depends, HTTPException
from typing import List
from utils import ensure_file_uploaded, process_stock_data
from stock_file_manager import StockFileManager
from stock_analyzer import StockAnalyzer

stock_router = APIRouter()

@stock_router.get("/stocks/jangta", response_model=List[str])
def get_stocks_jangta(file_path: str = Depends(ensure_file_uploaded)):
    stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
    stock_data = StockAnalyzer.calculate_vwap_with_pykrx(stock_codes)
    filtered_stocks = process_stock_data(stock_data)
    return [str(i) for i in filtered_stocks]

@stock_router.get("/stocks/danta", response_model=List[str])
def get_stocks_danta(days_ago: int = 2, file_path: str = Depends(ensure_file_uploaded)):
    stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
    today = StockAnalyzer.get_date_n_days_ago(days_ago)
    stock_data = StockAnalyzer.get_stock_data_for_date(stock_codes, today)
    filtered_stocks = process_stock_data(stock_data)
    return [str(i) for i in filtered_stocks]

@stock_router.get("/stocks/within-channel-range", response_model=List[str])
def get_stocks_within_channel_range(file_path: str = Depends(ensure_file_uploaded)):
    stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
    stocks_within_range = []
    for stock_code in stock_codes:
        df = StockAnalyzer.get_data_with_price_channel(stock_code)
        latest_data = df.iloc[-1]
        stocks_within_range.append(StockAnalyzer.is_close_within_range_of_lower_channel(stock_code, latest_data))
    non_zero_stock_data = [i for i in stocks_within_range if len(i) != 0 or len(i) != 1]
    filtered_stocks = process_stock_data(non_zero_stock_data)
    return [str(i) for i in filtered_stocks]
