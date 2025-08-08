from files.models import generate_tasks
from files.utils import extract_text_markdown, extract_text_using_pymupdf, extract_text_using_ocr
from fastapi import APIRouter, UploadFile
import os
from files.payloads import Text


file_router = APIRouter()


"""
    The code tries to extracts using md and ocr.
    if md doesn't exist, then it uses ocr
"""
@file_router.post("/upload")
async def upload_PDF(file: UploadFile):
    if (file is not None and file.filename):
        path: str  = file.filename
        ocr_text: str = ""
        pymupdf_text:str = ""
        md: str = ""
        with open (path, "wb") as f:
            f.write(await file.read()) # creates a local file to read
            ocr_text = extract_text_using_ocr(path)
            pymupdf_text = extract_text_using_pymupdf(path)
            md = extract_text_markdown(path)
            
            f.close()
            
        await file.close()
        
        os.remove(path) # removes the local file
        

        results: str = generate_tasks(md if md != "" else ocr_text) # use the markdown text if it exists, else use the ocr text
        
        # results = ""
        return {"filename": file.filename, "ocr": ocr_text, "pymupdf": pymupdf_text, "md": md, "results": results }
    else:
        return {
            "error": "missing file"
        }
        
@file_router.post("/text-upload")
async def upload_text(payload: Text):
    text = payload.text
    print(text)
    results = generate_tasks(text)
    return { "results": results }