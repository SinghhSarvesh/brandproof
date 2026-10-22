import pytest
from config import database_url


@pytest.mark.parametrize(
    "original,expected",
    [
        ("postgres://user:secret@db/app", "postgresql+psycopg://user:secret@db/app"),
        (
            "postgresql://user:secret@db/app?sslmode=require",
            "postgresql+psycopg://user:secret@db/app?sslmode=require",
        ),
        (
            "postgresql+psycopg://user:secret@db/app",
            "postgresql+psycopg://user:secret@db/app",
        ),
        ("sqlite:///./brandproof.db", "sqlite:///./brandproof.db"),
    ],
)
def test_database_url_uses_installed_driver(original, expected):
    assert database_url(original) == expected
