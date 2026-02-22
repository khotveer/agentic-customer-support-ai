
from models import generate_text
from prompts import get_risk_prmpt


ALLOWED_RISK_LEVELS = {"low", "low." "low_risk", "medium", "high", "high.", "high_risk"}


def assess_risk(query: str, intent: str, issue: str) -> str:
    """
    Assesses the escalation risk level of the customer query.
    Returns: low | medium | high
    """

    prompt = get_risk_prmpt(query)


    response = generate_text(
        prompt,
        max_new_tokens=20,
        temperature=0.0,
        do_sample=False,
    )

    response = response.strip().lower()

    candidate = response.split("answer:")[-1].lower().replace(".", "").strip()

    if candidate.lower() in ALLOWED_RISK_LEVELS:
        return candidate

    # Absolute safety fallback: never under-escalate
    return "high"