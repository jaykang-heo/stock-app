import os
from fastapi import HTTPException
from stock_analyzer import StockAnalyzer

uploaded_file_path = ""

def ensure_file_uploaded():
    if not uploaded_file_path or not os.path.exists(uploaded_file_path):
        raise HTTPException(status_code=400, detail="CSV file not uploaded yet")
    return uploaded_file_path

def save_uploaded_file(uploaded_file, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())

def process_stock_data(stock_data):
    stock_data_sorted = sorted(stock_data, key=lambda x: x[2], reverse=True)
    return StockAnalyzer.filter_stocks(stock_data_sorted)
