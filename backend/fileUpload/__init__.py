from fileUpload.helper import extract_text_using_pymupdf
from fastapi import APIRouter, File, UploadFile

file_router = APIRouter()

@file_router.post("/upload")
async def upload_PDF(file: UploadFile):
 
    
    path = file.filename
    with open (path, "wb") as f:
        f.write(await file.read())
        print(f.read())
        extract_text_using_pymupdf(path)
    return {"message": file.filename}