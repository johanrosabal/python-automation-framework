# mock/db/user_db.py
import json
from pathlib import Path
from typing import Dict, List
from models.user import User

# Path to the JSON file (inside mock/api/data/)
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "users.json"

# Ensure the folder exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_users() -> List[Dict]:
    """Load users from JSON file. Returns empty list if file is empty, missing, or invalid."""
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        try:
            data = json.loads(content)
            # Ensure we always return a list
            if isinstance(data, dict):
                # If data is a dict (e.g., old format), convert to list of values
                return list(data.values())
            elif isinstance(data, list):
                return data
            else:
                return []  # Invalid JSON structure
        except json.JSONDecodeError:
            return []  # Corrupted JSON


def _save_users(users: List[Dict]):
    """Save users list to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def get_all_users() -> List[User]:
    users_data = _load_users()
    return [User(**user) for user in users_data]


def get_user_by_id(user_id: int) -> User | None:
    users = _load_users()
    for user in users:
        if user["id"] == user_id:
            return User(**user)
    return None


def create_user(user_data: dict) -> User:
    users = _load_users()  # Now guaranteed to be a list
    new_id = max([u["id"] for u in users], default=0) + 1
    new_user = {"id": new_id, **user_data}
    users.append(new_user)  # ✅ Safe: users is always a list
    _save_users(users)
    return User(**new_user)


def update_user(user_id: int, user_data: dict) -> User | None:
    users = _load_users()
    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i] = {"id": user_id, **user_data}
            _save_users(users)
            return User(**users[i])
    return None


def delete_user(user_id: int) -> bool:
    users = _load_users()
    initial_count = len(users)
    users = [u for u in users if u["id"] != user_id]
    if len(users) < initial_count:
        _save_users(users)
        return True
    return False