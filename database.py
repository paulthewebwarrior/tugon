"""SQLite database module for candidate and message storage."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_FILE = DATA_DIR / "tugon.db"

# Position order for proper hierarchy sorting
POSITION_ORDER = {
    "President": 1,
    "Vice President": 2,
    "Secretary": 3,
    "Treasurer": 4,
    "Auditor": 5,
    "Business Manager": 6,
    "Public Relations Officer": 7,
    "2nd Year Representative": 8,
    "3rd Year Representative": 9,
    "4th Year Representative": 10,
    "5th Year Representative": 11,
}


def get_position_order(position: str) -> int:
    """Return sort order for a position (lower = higher rank)."""
    return POSITION_ORDER.get(position, 99)


def get_db_connection() -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Initialize the database schema."""
    DATA_DIR.mkdir(exist_ok=True)
    
    with db_connection() as conn:
        cursor = conn.cursor()
        
        # Candidates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                tagline TEXT DEFAULT '',
                credentials TEXT DEFAULT '',
                bio TEXT DEFAULT '',
                photo TEXT DEFAULT 'images/default-candidate.svg',
                highlights TEXT DEFAULT '[]',
                plan_of_action TEXT DEFAULT '',
                council TEXT NOT NULL DEFAULT 'ENSC',
                created_at TEXT DEFAULT '2026-03-08'
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT DEFAULT '',
                message TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for common queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_council ON candidates(council)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_position ON candidates(position)")


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    """Convert a sqlite3.Row to a dictionary with proper type handling."""
    d = dict(row)
    # Parse highlights from JSON string
    if 'highlights' in d and isinstance(d['highlights'], str):
        try:
            d['highlights'] = json.loads(d['highlights'])
        except json.JSONDecodeError:
            d['highlights'] = []
    return d


# ============== Candidate Operations ==============

def load_candidates() -> list[dict[str, Any]]:
    """Load all candidates from the database, sorted by council and position hierarchy."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM candidates")
        candidates = [row_to_dict(row) for row in cursor.fetchall()]
    # Sort by council, then position order, then name
    return sorted(candidates, key=lambda c: (c['council'], get_position_order(c['position']), c['name']))


def load_candidates_by_council(council_code: str) -> list[dict[str, Any]]:
    """Load candidates for a specific council, sorted by position hierarchy."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM candidates WHERE council = ?",
            (council_code.upper(),)
        )
        candidates = [row_to_dict(row) for row in cursor.fetchall()]
    # Sort by position order, then name
    return sorted(candidates, key=lambda c: (get_position_order(c['position']), c['name']))


def get_candidate(candidate_id: str) -> dict[str, Any] | None:
    """Get a single candidate by ID."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        row = cursor.fetchone()
        return row_to_dict(row) if row else None


def save_candidate(candidate: dict[str, Any]) -> None:
    """Insert or update a candidate."""
    highlights = candidate.get('highlights', [])
    if isinstance(highlights, list):
        highlights = json.dumps(highlights)
    
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO candidates 
            (id, name, position, tagline, credentials, bio, photo, highlights, plan_of_action, council, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate.get('id', ''),
            candidate.get('name', ''),
            candidate.get('position', ''),
            candidate.get('tagline', ''),
            candidate.get('credentials', ''),
            candidate.get('bio', ''),
            candidate.get('photo', 'images/default-candidate.svg'),
            highlights,
            candidate.get('plan_of_action', ''),
            candidate.get('council', 'ENSC').upper(),
            candidate.get('created_at', '2026-03-08')
        ))


def save_candidates(candidates: list[dict[str, Any]]) -> None:
    """Save multiple candidates (replaces all existing data)."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates")
        
        for candidate in candidates:
            highlights = candidate.get('highlights', [])
            if isinstance(highlights, list):
                highlights = json.dumps(highlights)
            
            cursor.execute("""
                INSERT INTO candidates 
                (id, name, position, tagline, credentials, bio, photo, highlights, plan_of_action, council, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                candidate.get('id', ''),
                candidate.get('name', ''),
                candidate.get('position', ''),
                candidate.get('tagline', ''),
                candidate.get('credentials', ''),
                candidate.get('bio', ''),
                candidate.get('photo', 'images/default-candidate.svg'),
                highlights,
                candidate.get('plan_of_action', ''),
                candidate.get('council', 'ENSC').upper(),
                candidate.get('created_at', '2026-03-08')
            ))


def delete_candidate(candidate_id: str) -> bool:
    """Delete a candidate by ID. Returns True if deleted."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
        return cursor.rowcount > 0


# ============== Message Operations ==============

def load_messages() -> list[dict[str, Any]]:
    """Load all messages from the database."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]


def save_message(message: dict[str, Any]) -> int:
    """Save a new message. Returns the message ID."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (name, email, subject, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            message.get('name', ''),
            message.get('email', ''),
            message.get('subject', ''),
            message.get('message', ''),
            message.get('created_at', '')
        ))
        return cursor.lastrowid or 0


def delete_message(message_id: int) -> bool:
    """Delete a message by ID. Returns True if deleted."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        return cursor.rowcount > 0


# Initialize database on module import
init_db()
