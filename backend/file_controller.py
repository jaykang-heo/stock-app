from fastapi import APIRouter, UploadFile, File
import os
from file_config import FileConfig  # Import the new class

router = APIRouter()


@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Get the original filename
    original_filename = file.filename

    # Construct the file location using the original filename
    file_location = f"uploads/{original_filename}"

    # Save the uploaded file to the constructed file location
    save_uploaded_file(file, file_location)

    # Set the file path in your configuration
    FileConfig.set_uploaded_file_path(file_location)

    print(f"File uploaded to: {FileConfig.get_uploaded_file_path()}")

    # Return the original filename in the response
    return {"filename": original_filename}


def save_uploaded_file(uploaded_file, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())
