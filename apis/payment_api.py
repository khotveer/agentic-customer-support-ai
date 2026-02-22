
from apis.supabase_client import fetch_table


def get_payment_data(account_id: str) -> dict | None:
    """
    Fetch payment status for a given account_id.
    """
    data = fetch_table("account_payment_status")

    matches = [x for x in data if x["account_id"] == account_id]

    return matches[0] if matches else None