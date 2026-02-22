
from models import generate_text
from prompts import get_faq_res_prmpt


def generate_faq_response(query: str, context: str) -> str:
    """
    Generates a FAQ-style answer strictly grounded in the provided context.
    If the answer is not present in the context, the model must return
    the exact fallback sentence defined in the prompt.
    """

    prompt = get_faq_res_prmpt(query, context)


    response = generate_text(
        prompt,
        max_new_tokens=120,
        temperature=0.0,
        do_sample=False,
    )

    response = response.strip()

    # Defensive cleanup if model echoes headers
    if "Final Answer:" in response:
        response = response.split("Final Answer:")[-1].strip()

    if "Answer:" in response:
        response = response.split("Answer:")[-1].strip()

    return response