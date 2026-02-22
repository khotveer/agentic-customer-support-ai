# pipeline/decision_engine.py

from classifiers.intent import classify_intent
from classifiers.issue import classify_issue
from classifiers.risk import assess_risk
from classifiers.data_required import requires_customer_data


def run_decision_engine(query: str) -> dict:
    """
    Runs all classification layers and returns structured decision attributes.
    """

    intent = classify_intent(query)
    issue = classify_issue(query)
    risk_level = assess_risk(query, intent, issue)

    if risk_level == "high":
        return {
            "query": query,
            "intent": intent,
            "issue": issue,
            "risk_level": risk_level,
            "data_dependency": "NA",
            "answerability": "escalate",
        }

    data_dependency = requires_customer_data(
        query=query,
        intent=intent,
        issue=issue,
        risk_level=risk_level,
    )

    if data_dependency == "yes":
        answerability = "api"
    else:
        answerability = "faq"

    return {
        "query": query,
        "intent": intent,
        "issue": issue,
        "risk_level": risk_level,
        "data_dependency": data_dependency,
        "answerability": answerability,
    }