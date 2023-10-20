from fastapi import APIRouter, Depends
from fastapi import FastAPI, HTTPException, Depends
from typing import List

from stock_file_manager import StockFileManager
from stock_analyzer import StockAnalyzer
from file_config import FileConfig  # Import the new class
import os

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


@router.get("/stocks/chart/candle/{stockCode}", response_model=str)
def get_stocks_candle_chart(stockCode: str):
    StockAnalyzer.draw_candle_chart(stockCode)  # This remains unchanged


@router.get("/stocks/chart/candle/{stockCode}", response_model=str)
def get_stocks_candle_chart(stockCode: str):
    StockAnalyzer.draw_candle_chart(stockCode)


def process_stock_data(stock_data):
    stock_data_sorted = sorted(stock_data, key=lambda x: x[2], reverse=True)
    return StockAnalyzer.filter_stocks(stock_data_sorted)
