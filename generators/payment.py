
from models import generate_text
from prompts import get_payment_res_prmpt


def generate_payment_response(query: str, payment_data: dict) -> str:
    """
    Generates a customer-facing payment status explanation
    using strictly provided payment data.
    """

    prompt = get_payment_res_prmpt(query, payment_data)


    response = generate_text(
        prompt,
        max_new_tokens=120,
        temperature=0.0,
        do_sample=False,
    )

    # Clean output
    response = response.strip()

    # Defensive cleanup in case model echoes headers
    if "FINAL ANSWER" in response:
        response = response.split("FINAL ANSWER")[-1].strip()

    return response