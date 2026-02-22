# vector_db/vector_db_load.py

import faiss
from vector_db.utils import load_pickle


def load_vector_db(index_path: str, data_path: str):
    index = faiss.read_index(index_path)
    rag_documents = load_pickle(data_path)
    return index, rag_documents