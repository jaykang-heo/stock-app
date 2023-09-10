from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import UploadFile, Form, Depends
from fastapi.param_functions import File
from stock_service import get_stock_codes_from_csv, get_date_n_days_ago, get_stock_data_for_date, filter_stocks, \
    calculate_vwap_with_pykrx
import os

app = FastAPI()

uploaded_file_path = ""
@app.get("/stocks/jangta", response_model=List[str])
def get_filtered_stocks():
    if not uploaded_file_path or not os.path.exists(uploaded_file_path):
        raise HTTPException(status_code=400, detail="CSV file not uploaded yet")

    stock_codes = get_stock_codes_from_csv(uploaded_file_path)

    stock_data = calculate_vwap_with_pykrx(stock_codes)
    print(stock_data)

    stock_data_sorted = sorted(stock_data, key=lambda x: x[2], reverse=True)
    filtered_stocks = filter_stocks(stock_data_sorted)
    print(filtered_stocks)

    # Optionally delete the file after processing
    # os.remove(uploaded_file_path)

    return [str(i) for i in filtered_stocks]


@app.get("/stocks/danta", response_model=List[str])
def get_filtered_stocks(days_ago: int = 2):
    if not uploaded_file_path or not os.path.exists(uploaded_file_path):
        raise HTTPException(status_code=400, detail="CSV file not uploaded yet")

    stock_codes = get_stock_codes_from_csv(uploaded_file_path)

    today = get_date_n_days_ago(days_ago)
    stock_data = get_stock_data_for_date(stock_codes, today)

    stock_data_sorted = sorted(stock_data, key=lambda x: x[2], reverse=True)
    filtered_stocks = filter_stocks(stock_data_sorted)
    print(filtered_stocks)

    # Optionally delete the file after processing
    # os.remove(uploaded_file_path)

    return [str(i) for i in filtered_stocks]

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    global uploaded_file_path
    file_location = f"uploads/{file.filename}"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    uploaded_file_path = file_location
    return {"filename": file.filename}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
