
from apis.supabase_client import fetch_table


def get_transaction_data(account_id: str) -> dict | None:
    """
    Fetch billing summary for a given account_id.
    """
    data = fetch_table("account_billing_summary")

    matches = [x for x in data if x["account_id"] == account_id]

    return matches[0] if matches else None