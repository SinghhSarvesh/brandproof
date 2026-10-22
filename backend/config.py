"""Configuration helpers shared by local and hosted deployments."""


def database_url(value: str) -> str:
    """Use the installed psycopg 3 driver for provider-issued Postgres URLs."""
    for prefix in ("postgres://", "postgresql://"):
        if value.startswith(prefix):
            return "postgresql+psycopg://" + value[len(prefix) :]
    return value
