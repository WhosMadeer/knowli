import pymupdf
import pymupdf4llm
# import os

"""
    extract_text_using_pymupdf only works with PDFs that aren't based around image based PDFs 
    PDFs created with Canva or other tools will not work with this function
"""

def extract_text_using_pymupdf(file: str):
    doc = pymupdf.open(file)
    text = ""
    
    for page in doc:
        page_text = page.get_text()
        if (page_text):
            text += page_text
        
    doc.close()
    
    return text

"""
    extract_text_using_ocr extracts
"""
def extract_text_using_ocr(file: str):
    doc = pymupdf.open(file)
    text = ""
    
    for page in doc:
        tp = page.get_textpage_ocr()
        page_text = page.get_text(textpage=tp)     
        if (page_text):       
            text += page_text
        
    doc.close()
    
    return text


def extract_text_markdown(file: str):
    text = pymupdf4llm.to_markdown(file)
    
    return text
