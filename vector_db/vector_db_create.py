# vector_db/vector_db_create.py

import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

from vector_db.utils import (
    normalize_text,
    get_sections,
    chunk_text_by_size,
    save_pickle,
)


def get_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += "\n" + text

    return full_text


def get_rag_documents(sections):
    rag_documents = []

    for section in sections:
        chunks = chunk_text_by_size(section["content"])

        for idx, chunk in enumerate(chunks):
            rag_documents.append({
                "text": chunk,
                "metadata": {
                    "section_number": section["section_number"],
                    "section_title": section["section_title"],
                    "chunk_index": idx,
                },
            })

    return rag_documents


def create_vector_database(embeddings, index_path: str):
    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, index_path)
    print("FAISS index saved. Total vectors:", index.ntotal)


def create_vector_embeddings_and_save(
    pdf_path: str,
    index_path: str,
    data_path: str,
    device: str = "cpu",
):
    full_text = get_pdf_text(pdf_path)
    full_text = normalize_text(full_text)

    sections = get_sections(full_text)
    rag_documents = get_rag_documents(sections)

    save_pickle(data_path, rag_documents)

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2",
        device=device
    )

    embeddings = embedding_model.encode(
        [doc["text"] for doc in rag_documents],
        show_progress_bar=True,
    )

    create_vector_database(embeddings, index_path)

    return index_path, data_path