from fastapi import APIRouter, UploadFile, File
from utils import save_uploaded_file

upload_router = APIRouter()
uploaded_file_path = ""

@upload_router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    global uploaded_file_path
    file_location = f"uploads/{file.filename}"
    save_uploaded_file(file, file_location)
    uploaded_file_path = file_location
    return {"filename": file.filename}
