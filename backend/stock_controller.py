from fastapi import APIRouter, Depends
from fastapi import FastAPI, HTTPException, Depends
from typing import List

from joongta_service import calculat_joongta
from stock_file_manager import StockFileManager
from stock_analyzer import StockAnalyzer
from file_config import FileConfig  # Import the new class
import os
import plotly.graph_objects as go
from pykrx import stock

router = APIRouter()

def ensure_file_uploaded():
    if not FileConfig.get_uploaded_file_path() or not os.path.exists(FileConfig.get_uploaded_file_path()):
        raise HTTPException(status_code=400, detail="CSV file not uploaded yet")
    return FileConfig.get_uploaded_file_path()



@router.get("/stocks/jangta", response_model=List[str])
def get_stocks_jangta(days_ago: int = 0, file_path: str = Depends(ensure_file_uploaded)):
    if "test" in file_path:
        stock_codes = StockFileManager.get_stock_codes_from_txt(file_path)
    else:
        stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
    print(stock_codes)
    today = StockAnalyzer.get_date_n_days_ago(days_ago)
    stock_data = StockAnalyzer.analyze_stocks(stock_codes, today)
    print(stock_data)
    filtered_stocks = set(process_stock_data(stock_data))
    return [str(i) for i in filtered_stocks]

@router.get("/stocks/joongta", response_model=List[str])
def get_stocks_joongta(file_path: str = Depends(ensure_file_uploaded)):
    stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
    stock_data = StockAnalyzer.fetch_stock_data(stock_codes, StockAnalyzer.TODAY)  # Changed the method here
    filtered_stocks = process_stock_data(stock_data)
    return [str(i) for i in filtered_stocks]

@router.get("/stocks/danta", response_model=List[str])
def get_stocks_danta(days_ago: int = 2, file_path: str = Depends(ensure_file_uploaded)):
    stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
    today = StockAnalyzer.get_date_n_days_ago(days_ago)
    stock_data = StockAnalyzer.fetch_stock_data(stock_codes, today)  # Changed the method here
    filtered_stocks = process_stock_data(stock_data)
    return [str(i) for i in filtered_stocks]

@router.get("/stocks/within-channel-range", response_model=List[str])
def get_stocks_within_channel_range(file_path: str = Depends(ensure_file_uploaded)):
    stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
    stocks_within_range = StockAnalyzer.is_close_within_range_of_lower_channel(stock_codes)
    filtered_stocks = process_stock_data(stocks_within_range)
    return [str(i) for i in filtered_stocks]

@router.get("/stocks/chart/candle/{stockCode}", response_model=str)
def get_stocks_candle_chart(stockCode: str):
    StockAnalyzer.draw_candle_chart(stockCode)  # This remains unchanged


@router.get("/stocks/chart/candle/{stockCode}", response_model=str)
def get_stocks_candle_chart(stockCode: str):
    StockAnalyzer.draw_candle_chart(stockCode)

def process_stock_data(stock_data):
    stock_data_sorted = sorted(stock_data, key=lambda x: x[2], reverse=True)
    return StockAnalyzer.filter_stocks(stock_data_sorted)
