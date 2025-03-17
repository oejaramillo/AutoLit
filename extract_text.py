import fitz  # PyMuPDF
import os
import concurrent.futures
from config import PDF_FOLDER, TEXT_FOLDER

os.makedirs(TEXT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])

def process_pdf(filename):
    if filename.endswith('.pdf'):
        file_path = os.path.join(PDF_FOLDER, filename)
        text = extract_text_from_pdf(file_path)
        output_path = os.path.join(TEXT_FOLDER, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return filename, text

def extract_texts():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return dict(executor.map(process_pdf, os.listdir(PDF_FOLDER)))

if __name__ == "__main__":
    extracted_texts = extract_texts()
    print("Extracción de texto completada.")
