# from fastapi import FastAPI, HTTPException, Depends
# from typing import List
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import UploadFile, File
# import os
# from stock_file_manager import StockFileManager
# from stock_analyzer import StockAnalyzer
#
#
# app = FastAPI()
#
# uploaded_file_path = ""
#
# # Separate out file validation
# def ensure_file_uploaded():
#     if not uploaded_file_path or not os.path.exists(uploaded_file_path):
#         raise HTTPException(status_code=400, detail="CSV file not uploaded yet")
#     return uploaded_file_path
#
# @app.get("/stocks/jangta", response_model=List[str])
# def get_stocks_jangta(file_path: str = Depends(ensure_file_uploaded)):
#     stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
#
#     stock_data = StockAnalyzer.calculate_vwap_with_pykrx(stock_codes)
#
#     filtered_stocks = process_stock_data(stock_data)
#     return [str(i) for i in filtered_stocks]
#
# @app.get("/stocks/danta", response_model=List[str])
# def get_stocks_danta(days_ago: int = 2, file_path: str = Depends(ensure_file_uploaded)):
#     stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
#
#     today = StockAnalyzer.get_date_n_days_ago(days_ago)
#     stock_data = StockAnalyzer.get_stock_data_for_date(stock_codes, today)
#
#     filtered_stocks = process_stock_data(stock_data)
#     return [str(i) for i in filtered_stocks]
#
# def process_stock_data(stock_data):
#     stock_data_sorted = sorted(stock_data, key=lambda x: x[2], reverse=True)
#     return StockAnalyzer.filter_stocks(stock_data_sorted)
#
# @app.post("/upload-csv/")
# async def upload_csv(file: UploadFile = File(...)):
#     global uploaded_file_path
#     file_location = f"uploads/{file.filename}"
#
#     save_uploaded_file(file, file_location)
#     uploaded_file_path = file_location
#     return {"filename": file.filename}
#
# def save_uploaded_file(uploaded_file, file_path):
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)
#     with open(file_path, "wb") as buffer:
#         buffer.write(uploaded_file.file.read())
#
# @app.get("/stocks/within-channel-range", response_model=List[str])
# def get_stocks_within_channel_range(file_path: str = Depends(ensure_file_uploaded)):
#     stock_codes = StockFileManager.get_stock_codes_from_csv(file_path)
#     stocks_within_range = StockAnalyzer.is_close_within_range_of_lower_channel(stock_codes)
#     filtered_stocks = process_stock_data(stocks_within_range)
#     return [str(i) for i in filtered_stocks]
#
# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Allow requests from this origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods
#     allow_headers=["*"],  # Allow all headers
# )
