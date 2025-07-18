import pymupdf

def extract_text_using_pymupdf(file):
    doc = pymupdf.open(file)
    print(doc)
    for page in doc:
        print(page.get_text())
        
    doc.close()
    # return doc