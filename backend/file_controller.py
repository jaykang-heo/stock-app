from fastapi import APIRouter, UploadFile, File
import os
from file_config import FileConfig  # Import the new class

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    default_filename = "stock.csv"
    file_location = f"uploads/{default_filename}"
    save_uploaded_file(file, file_location)
    FileConfig.set_uploaded_file_path(file_location)  # Use the class method to update the path
    print(f"File uploaded to: {FileConfig.get_uploaded_file_path()}")
    return {"filename": default_filename}

def save_uploaded_file(uploaded_file, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())
