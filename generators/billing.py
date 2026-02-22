# generators/billing.py

from models import generate_text
from prompts import get_billing_res_prmpt


def generate_billing_response(user_query: str, data: dict) -> str:
    """
    Generates a customer-facing billing explanation
    using strictly provided payment data.
    """

    prompt = get_billing_res_prmpt(user_query, data)


    response = generate_text(
        prompt,
        max_new_tokens=130,
        temperature=0.0,
        do_sample=False,
    )

    # Clean output
    response = response.strip()

    # Remove accidental leading headers if model adds anything
    if "FINAL ANSWER" in response:
        response = response.split("FINAL ANSWER")[-1].strip()

    return response