import os
import dotenv

dotenv.load_dotenv()

# Rutas de archivos
PDF_FOLDER = "./pdfs"
TEXT_FOLDER = "./procesados"
OUTPUT_FOLDER = "./output"
INDEX_FILE = "./output/faiss_index.bin"
BIBTEX_FILE = "./references.bib"

# Claves API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
