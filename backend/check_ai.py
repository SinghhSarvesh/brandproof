"""Check live model connectivity and evidence validation using synthetic data only.

Run explicitly after adding provider variables. Makes one billable API request.
Never prints keys, provider responses or private content.
"""

import os
from app import semantic

if __name__ == "__main__":
    if not os.getenv("AI_API_KEY") or not os.getenv("AI_MODEL"):
        raise SystemExit(
            "Set AI_API_KEY and AI_MODEL in backend service variables first."
        )
    source = {
        "id": 1,
        "title": "Synthetic battery specification",
        "version": 1,
        "text": "Northstar One provides up to 12 hours of battery life.",
    }
    draft = {
        "text": "Northstar One provides 20 hours of battery life.",
        "purpose": "Announce the product using approved specifications.",
        "audience": "Customers",
    }
    try:
        results = semantic(draft, [source])
    except Exception:
        raise SystemExit(
            "AI check failed. Verify the key, model access, quota, endpoint and JSON support. No secrets or provider response were logged."
        )
    if not any(item["category"] == "contradiction" for item in results):
        raise SystemExit(
            "The model responded but missed the synthetic contradiction. Do not treat this as a validated configuration."
        )
    print(
        "AI connection and citation validation passed for one synthetic contradiction. This is not an accuracy evaluation."
    )
