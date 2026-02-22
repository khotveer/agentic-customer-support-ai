
from models import generate_text
from prompts import get_data_req_prmt


def requires_customer_data(
    query: str,
    intent: str,
    issue: str,
    risk_level: str
) -> str:
    """
    Determines whether customer-specific data is required.
    Returns: yes | no
    """

    # This function should never be called for high risk,
    # but we guard anyway.
    if risk_level == "high":
        return "yes"

    prompt = get_data_req_prmt(query, intent, issue)


    response = generate_text(
        prompt,
        max_new_tokens=25,
        temperature=0.0,
        do_sample=False,
    )

    response = response.strip().lower()

    candidate = response.split("answer:")[-1].replace(".", "").strip()

    if candidate in {"yes", "no"}:
        return candidate

    # Safety rule: default to yes
    return "yes"