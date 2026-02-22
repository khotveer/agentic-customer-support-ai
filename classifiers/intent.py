from models import generate_text
from prompts import get_intent_prmpt


def classify_intent(customer_message: str) -> str:
    prompt = get_intent_prmpt(customer_message)


    response = generate_text(
        prompt,
        max_new_tokens=4,
        temperature=0.0,
        do_sample=False
    )

    label = response.split("Answer:")[-1].strip().lower()

    if label in {"complaint", "request", "inquiry"}:
        return label

    return "inquiry"