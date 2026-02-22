
import os
import requests


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def _get_headers():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Supabase credentials not set in environment variables")

    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


def fetch_table(table_name: str) -> list:
    """
    Fetches all rows from a Supabase table.
    """
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/{table_name}",
        headers=_get_headers(),
    )

    response.raise_for_status()
    return response.json()