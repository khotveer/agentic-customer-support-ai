# pipeline/orchestrator.py

from pipeline.decision_engine import run_decision_engine
from pipeline.router import (
    handle_api_flow,
    handle_faq_flow,
    handle_escalation,
)
from evaluation.stability import evaluate_consistency


def process_query(
    query: str,
    account_id: str,
    index,
    embedding_model,
    rag_documents: list,
    include_stability: bool = True,
) -> dict:
    """
    End-to-end processing of a customer query.
    """

    decision = run_decision_engine(query)

    if decision["answerability"] == "api":
        response = handle_api_flow(decision, account_id)

    elif decision["answerability"] == "faq":
        response = handle_faq_flow(
            query=query,
            index=index,
            embedding_model=embedding_model,
            rag_documents=rag_documents,
        )

    else:
        response = handle_escalation()

    result = {
        "decision": decision,
        "response": response,
    }

    if include_stability:
        stability_score = evaluate_consistency(
            query,
            decision["intent"],
            decision["issue"],
        )
        result["stability_score"] = stability_score

    return result