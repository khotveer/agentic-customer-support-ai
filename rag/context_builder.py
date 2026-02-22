# rag/context_builder.py

from rag.retriever import retrieve_top_k


def build_context_for_llm(
    query: str,
    index,
    embedding_model,
    rag_documents: list,
    top_k: int = 5,
    max_chars_per_chunk: int = 300,
) -> str:
    """
    Builds a formatted context string for LLM consumption
    from top-k retrieved RAG documents.
    """

    results = retrieve_top_k(
        query=query,
        index=index,
        embedding_model=embedding_model,
        rag_documents=rag_documents,
        top_k=top_k,
    )

    context_parts = []

    for r in results:
        meta = r["metadata"]
        text = r["text"][:max_chars_per_chunk]

        context_parts.append(
            f"Section {meta['section_number']} - {meta['section_title']}\n{text}"
        )

    return "\n\n".join(context_parts)