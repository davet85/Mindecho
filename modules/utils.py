import json
from pathlib import Path
from datetime import datetime

PROFILE_PATH = Path("database/user_profile.json")

def save_profile(profile: dict):
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROFILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

def load_profile() -> dict:
    if PROFILE_PATH.exists():
        with PROFILE_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def days_since(date_str: str) -> int:
    """Return number of days since date string in YYYY-MM-DD."""
    if not date_str:
        return 0
    try:
        past = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (datetime.now().date() - past).days
    except:
        return 0

def get_weakest_domain(domains: dict) -> str:
    """Returns the lowest scoring domain key."""
    return min(domains, key=domains.get)
