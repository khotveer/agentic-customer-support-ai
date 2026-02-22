
from models import generate_text
from prompts import get_consistency_prmpt


def _parse_boolean_answer(response: str) -> bool | None:
    """
    Safely parse True / False from model output.
    Returns None if parsing fails.
    """
    response = response.lower()

    if "true" in response:
        return True
    if "false" in response:
        return False

    return None


def evaluate_consistency(query: str, intent: str, issue: str) -> float:
    """
    Measures self-consistency of intent and issue classification
    using multiple LLM passes.

    Returns a stability score between 0.0 and 1.0.
    This score MUST NOT be used for routing or escalation.
    """

    prompt = get_consistency_prmpt(query, intent, issue)

    temperatures = [0.0, 0.3, 0.5]
    results = []

    for temp in temperatures:
        response = generate_text(
            prompt,
            max_new_tokens=64,
            temperature=temp,
            do_sample=(temp > 0.0),
        )

        parsed = _parse_boolean_answer(response)
        if parsed is not None:
            results.append(parsed)

    if not results:
        return 0.0

    # True → 1, False → 0
    return sum(1 for r in results if r) / len(results)