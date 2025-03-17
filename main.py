from extract_text import extract_texts
from classify_articles import build_faiss_index, load_faiss_index
from summarize_articles import extract_key_info
from generate_review import generate_literature_review, save_review

def main():
    print("🚀 Iniciando proceso de revisión de literatura...")
    
    # 1️⃣ Extraer texto de PDFs
    extracted_texts = extract_texts()
    
    # 2️⃣ Construir índice FAISS (si no existe)
    index = load_faiss_index()
    if not index:
        index = build_faiss_index(extracted_texts.values())
        print("Índice FAISS creado.")

    # 3️⃣ Extraer información clave de los artículos
    summaries = {filename: extract_key_info(text) for filename, text in extracted_texts.items()}
    
    # 4️⃣ Generar revisión de literatura
    summaries_text = "\n\n".join([f"### {k}\n{v}" for k, v in summaries.items()])
    review_text = generate_literature_review(summaries_text)
    
    # 5️⃣ Guardar revisión final
    save_review(review_text)
    
    print("✅ Revisión de literatura completada.")

if __name__ == "__main__":
    main()
