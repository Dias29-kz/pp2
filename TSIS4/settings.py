"""
settings.py — load / save user preferences to settings.json.

Structure of settings.json:
{
    "snake_color": [0, 200, 0],
    "grid_overlay": false,
    "sound":        true
}
"""

import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

DEFAULTS = {
    "snake_color": [0, 200, 0],
    "grid_overlay": False,
    "sound":        True,
}


def load() -> dict:
    """Return settings dict, creating the file with defaults if absent."""
    if not os.path.exists(SETTINGS_FILE):
        save(DEFAULTS.copy())
        return DEFAULTS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Fill in any missing keys with defaults
        for key, val in DEFAULTS.items():
            data.setdefault(key, val)
        return data
    except Exception as e:
        print(f"[Settings] Load error: {e} — using defaults.")
        return DEFAULTS.copy()


def save(data: dict) -> bool:
    """Persist settings dict to settings.json.  Returns True on success."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"[Settings] Save error: {e}")
        return False