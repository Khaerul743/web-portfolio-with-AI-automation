import os
import requests
import fitz  # PyMuPDF

def download_pdf_text(pdf_url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(pdf_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to download Pdf.")
    
    path = "pdf/scholar.pdf"
    with open(path, "wb") as f:
        f.write(response.content)

    doc = fitz.open("pdf/scholar.pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    doc.close()
    if os.path.exists(path):
        os.remove(path)
    return full_text[int((len(full_text)/2))]

if __name__ == "__main__":
    text = download_pdf_text("https://www.jurnal-id.com/index.php/jupin/article/download/874/420")

    print(text)
