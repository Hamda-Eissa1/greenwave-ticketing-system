# storage/data_manager.py
import pickle
import os
from typing import Any

# Save data files inside project_root/storage/data/
ROOT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "data")
os.makedirs(ROOT_DATA_DIR, exist_ok=True)

def _fullpath(filename: str) -> str:
    return os.path.join(ROOT_DATA_DIR, filename)

def save_data(filename: str, data: Any) -> None:
    """Serialize data to filename (binary)."""
    full = _fullpath(filename)
    # ensure directory exists
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_data(filename: str) -> Any:
    """Load and return object from filename. Returns default empty list if not present."""
    full = _fullpath(filename)
    try:
        with open(full, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        # If the file is corrupted or can't be unpickled, return empty list to avoid crash.
        return []
