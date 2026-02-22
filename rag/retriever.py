# rag/retriever.py

import numpy as np


def retrieve_top_k(
    query: str,
    index,
    embedding_model,
    rag_documents: list,
    top_k: int = 5,
):
    """
    Retrieves top-k most relevant RAG documents for a query.
    """

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(rag_documents):
            results.append(rag_documents[idx])

    return results