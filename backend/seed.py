"""Idempotent demo setup; public demo mode syncs synthetic account passwords."""

import os
from sqlalchemy import select
from app import Base, engine, SessionLocal, User, Record, password_hash, insert


def seed():
    password = os.getenv("DEMO_PASSWORD", "")
    if len(password) < 12:
        raise SystemExit("Set DEMO_PASSWORD to at least 12 characters before seeding.")
    Base.metadata.create_all(engine)
    with SessionLocal() as s:
        for role in ["manager", "creator", "reviewer"]:
            email = role + "@brandproof.demo"
            existing = s.scalar(select(User).where(User.email == email))
            if not existing:
                s.add(
                    User(
                        org="northstar",
                        email=email,
                        role=role,
                        password=password_hash(password),
                    )
                )
            elif os.getenv("DEMO_QUICK_FILL") == "true":
                if existing.org != "northstar" or existing.role != role:
                    raise SystemExit("Demo account identity mismatch; refusing password update.")
                existing.password = password_hash(password)
        s.flush()
        u = s.scalar(select(User).where(User.email == "manager@brandproof.demo"))
        if not s.scalar(
            select(Record).where(Record.org == "northstar", Record.kind == "source")
        ):
            for title, kind, text, match, replacement in [
                (
                    "Battery life specification",
                    "fact",
                    "Up to 12 hours of battery life.",
                    "battery life",
                    "",
                ),
                (
                    "Ranking claims policy",
                    "claim",
                    "Ranking claims require current approved substantiation. No approved ranking evidence exists for this demo.",
                    "India’s No. 1",
                    "",
                ),
                (
                    "Ranking claims policy ASCII",
                    "claim",
                    "Ranking claims require current approved substantiation. No approved ranking evidence exists for this demo.",
                    "India's No. 1",
                    "",
                ),
                (
                    "Product naming",
                    "term",
                    "Use Northstar One as the product name.",
                    "NS1",
                    "Northstar One",
                ),
                (
                    "Voice and tone",
                    "tone",
                    "Use clear, helpful language. Avoid exaggerated urgency, intimidation and insults.",
                    "",
                    "",
                ),
                (
                    "Social image dimensions",
                    "dimension",
                    "Social square creative must be 1080 by 1080 pixels.",
                    "1080x1080",
                    "",
                ),
            ]:
                insert(
                    s,
                    u,
                    "source",
                    {
                        "title": title,
                        "kind": kind,
                        "text": text,
                        "match": match,
                        "replacement": replacement,
                        "valid_from": "",
                        "valid_until": "",
                        "active": True,
                        "scope": "social" if kind == "dimension" else "all",
                        "version": 1,
                        "owner": u.email,
                        "supersedes": None,
                    },
                )
        s.commit()
    print(
        "Demo prepared: manager@brandproof.demo, creator@brandproof.demo, reviewer@brandproof.demo. Passwords sync only when DEMO_QUICK_FILL=true."
    )


if __name__ == "__main__":
    seed()
