# pipeline/router.py

from apis import get_transaction_data, get_payment_data
from generators.billing import generate_billing_response
from generators.payment import generate_payment_response
from generators.faq import generate_faq_response
from rag import build_context_for_llm


def handle_escalation() -> str:
    return (
        "Your concern requires additional review due to its sensitive nature. "
        "It has been flagged for appropriate handling to ensure it is addressed correctly."
    )


def handle_api_flow(decision: dict, account_id: str) -> str:
    issue_type = decision["issue"]
    query = decision["query"]

    if issue_type == "billing_issue":
        data = get_transaction_data(account_id)
        if not data:
            return "Unable to retrieve billing details at the moment."
        return generate_billing_response(query, data)

    if issue_type == "payment_issue":
        data = get_payment_data(account_id)
        if not data:
            return "Unable to retrieve payment details at the moment."
        return generate_payment_response(query, data)

    return "This issue type is not supported via API flow."


def handle_faq_flow(
    query: str,
    index,
    embedding_model,
    rag_documents: list,
) -> str:
    context = build_context_for_llm(
        query=query,
        index=index,
        embedding_model=embedding_model,
        rag_documents=rag_documents,
    )

    return generate_faq_response(query, context)