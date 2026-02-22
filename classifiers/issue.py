
from models import generate_text
from prompts import get_issue_prmpt


ALLOWED_ISSUES = {
    "billing_issue",
    "payment_issue",
    "refund_issue",
    "account_issue",
    "technical_issue",
    "delivery_issue",
    "service_issue",
    "pricing_issue",
    "other_issue",
}


def classify_issue(customer_message: str) -> str:
    """
    Classifies the customer message into a single issue label.
    Returns one of the predefined issue labels.
    """

    prompt = get_issue_prmpt(customer_message)


    response = generate_text(
        prompt,
        max_new_tokens=8,
        temperature=0.0,
        do_sample=False,
    )

    # Clean and extract label safely
    response = response.strip().lower()

    # Try to extract the last meaningful line
    lines = [line.strip() for line in response.splitlines() if line.strip()]
    if lines:
        candidate = lines[-1]
    else:
        candidate = response

    # Remove accidental punctuation
    candidate = candidate.replace(".", "").strip()

    if candidate in ALLOWED_ISSUES:
        return candidate

    # Safe fallback
    return "other_issue"