# core/memory.py
import json
import os
from datetime import datetime

DATA_DIR = "data"
MEMORY_FILE = os.path.join(DATA_DIR, "atlas_memory.json")

DEFAULT_DOC = {
    "profile": {
        "name": "Mac",
        "preferences": {}
    },
    "conversations": [],  # [{user, query, response, timestamp}]
    "knowledge": {
        "notes": []
    },
    "reminders": []
}

def _ensure_dirs():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def init_database():
    _ensure_dirs()
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DOC, f, indent=2)

def _read():
    _ensure_dirs()
    if not os.path.exists(MEMORY_FILE):
        init_database()
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # recover from a corrupted/empty file
            return DEFAULT_DOC.copy()

def _write(data: dict):
    _ensure_dirs()
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_user_memory():
    return _read()

def update_user_memory(data: dict):
    _write(data)

def save_conversation(user: str, query: str, response: str):
    data = _read()
    data["conversations"].append({
        "user": user,
        "query": query,
        "response": response,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })
    _write(data)

def add_reminder(text: str):
    data = _read()
    data["reminders"].append(text)
    _write(data)

def get_reminders():
    data = _read()
    return list(data.get("reminders", []))

def append_note(text: str):
    data = _read()
    data["knowledge"]["notes"].append({
        "text": text,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })
    _write(data)

def get_recent_conversations(n: int = 5):
    data = _read()
    return data.get("conversations", [])[-n:]
