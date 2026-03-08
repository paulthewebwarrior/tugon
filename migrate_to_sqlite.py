"""Migration script to import JSON data into SQLite database."""

import json
from pathlib import Path

# Initialize database schema
import database

DATA_DIR = Path(__file__).resolve().parent / "data"
CANDIDATES_JSON = DATA_DIR / "candidates.json"
MESSAGES_JSON = DATA_DIR / "messages.json"


def migrate_candidates() -> int:
    """Migrate candidates from JSON to SQLite."""
    if not CANDIDATES_JSON.exists():
        print("No candidates.json found, skipping...")
        return 0
    
    with open(CANDIDATES_JSON, "r", encoding="utf-8") as f:
        candidates = json.load(f)
    
    if not isinstance(candidates, list):
        print("Invalid candidates.json format")
        return 0
    
    count = 0
    for candidate in candidates:
        if isinstance(candidate, dict):
            database.save_candidate(candidate)
            count += 1
            print(f"  Migrated: {candidate.get('name', 'Unknown')}")
    
    return count


def migrate_messages() -> int:
    """Migrate messages from JSON to SQLite."""
    if not MESSAGES_JSON.exists():
        print("No messages.json found, skipping...")
        return 0
    
    with open(MESSAGES_JSON, "r", encoding="utf-8") as f:
        messages = json.load(f)
    
    if not isinstance(messages, list):
        print("Invalid messages.json format")
        return 0
    
    count = 0
    for message in messages:
        if isinstance(message, dict):
            database.save_message(message)
            count += 1
            print(f"  Migrated message from: {message.get('name', 'Unknown')}")
    
    return count


def main() -> None:
    """Run the migration."""
    print("=" * 50)
    print("Tugon JSON to SQLite Migration")
    print("=" * 50)
    
    print(f"\nDatabase location: {database.DATABASE_FILE}")
    print("\n[1/2] Migrating candidates...")
    candidate_count = migrate_candidates()
    print(f"  Total candidates migrated: {candidate_count}")
    
    print("\n[2/2] Migrating messages...")
    message_count = migrate_messages()
    print(f"  Total messages migrated: {message_count}")
    
    print("\n" + "=" * 50)
    print("Migration complete!")
    print(f"  - {candidate_count} candidates")
    print(f"  - {message_count} messages")
    print("=" * 50)
    
    # Verify by loading data back
    print("\nVerification:")
    loaded = database.load_candidates()
    print(f"  Candidates in database: {len(loaded)}")
    
    msgs = database.load_messages()
    print(f"  Messages in database: {len(msgs)}")


if __name__ == "__main__":
    main()
