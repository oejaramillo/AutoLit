import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from config import INDEX_FILE

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text)

def build_faiss_index(texts):
    embeddings = np.array([get_embedding(t) for t in texts], dtype=np.float32)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)
    return index

def load_faiss_index():
    if os.path.exists(INDEX_FILE):
        return faiss.read_index(INDEX_FILE)
    return None
