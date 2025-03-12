import pdfplumber

def text_extract (uploaad_doc):
    with pdfplumber.open(uploaad_doc) as file :
        text = ""
        for page in file.pages:
            page_text = page.extract_text()
            if page_text:
                text+=page_text +"/n"
    return text.strip()

 

