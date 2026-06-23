"""Persistent site counters stored in PostgreSQL."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any, Iterator

logger = logging.getLogger(__name__)

_COUNTERS = {
    "site_visits": "site_visits",
    "downloads": "downloads",
    "quizzes": "quizzes",
}

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS site_stats (
  id INT PRIMARY KEY DEFAULT 1,
  site_visits INT NOT NULL DEFAULT 0,
  downloads INT NOT NULL DEFAULT 0,
  quizzes INT NOT NULL DEFAULT 0,
  CONSTRAINT site_stats_singleton CHECK (id = 1)
);
INSERT INTO site_stats (id) VALUES (1)
ON CONFLICT (id) DO NOTHING;
"""


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def database_configured(config: Any) -> bool:
    return bool(getattr(config, "DATABASE_URL", "") or "")


@contextmanager
def _connection(database_url: str) -> Iterator[Any]:
    import psycopg2

    conn = psycopg2.connect(normalize_database_url(database_url))
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_stats_db(database_url: str) -> None:
    if not database_url:
        return
    with _connection(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(_SCHEMA_SQL)


def get_stats(database_url: str) -> dict[str, int] | None:
    if not database_url:
        return None
    try:
        with _connection(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT site_visits, downloads, quizzes FROM site_stats WHERE id = 1"
                )
                row = cur.fetchone()
                if not row:
                    return {"site_visits": 0, "downloads": 0, "quizzes": 0}
                return {
                    "site_visits": int(row[0]),
                    "downloads": int(row[1]),
                    "quizzes": int(row[2]),
                }
    except Exception:
        logger.exception("Failed to read site stats")
        return None


def format_compact_number(value: int | float) -> str:
    """Format large counts as 1.2K, 3.4M, 1.1B."""
    number = int(value)
    if number >= 1_000_000_000:
        scaled = number / 1_000_000_000
        suffix = "B"
    elif number >= 1_000_000:
        scaled = number / 1_000_000
        suffix = "M"
    elif number >= 1_000:
        scaled = number / 1_000
        suffix = "K"
    else:
        return str(number)

    text = f"{scaled:.1f}".rstrip("0").rstrip(".")
    return f"{text}{suffix}"


def increment_stat(database_url: str, counter: str) -> dict[str, int] | None:
    column = _COUNTERS.get(counter)
    if not column or not database_url:
        return None
    try:
        with _connection(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    UPDATE site_stats
                    SET {column} = {column} + 1
                    WHERE id = 1
                    RETURNING site_visits, downloads, quizzes
                    """
                )
                row = cur.fetchone()
                if not row:
                    init_stats_db(database_url)
                    return increment_stat(database_url, counter)
                return {
                    "site_visits": int(row[0]),
                    "downloads": int(row[1]),
                    "quizzes": int(row[2]),
                }
    except Exception:
        logger.exception("Failed to increment site stat %s", counter)
        return None
