# vdatabprot.py
# Mock implementation of the VDataBProt client

from typing import Optional, Dict

# In-memory dictionary to simulate a key-value store
_VDataBProt_store: Dict[str, str] = {}

def save(key: str, value: str):
    """Saves a value to the VDataBProt store."""
    try:
        _VDataBProt_store[key] = value
        print(f"[VDataBProt] Saved data for key: {key}")
    except Exception as e:
        print(f"ERROR: [VDataBProt] Failed to save data: {e}")

def load(key: str) -> Optional[str]:
    """Loads a value from the VDataBProt store."""
    try:
        value = _VDataBProt_store.get(key)
        if value:
            print(f"[VDataBProt] Loaded data for key: {key}")
            return value
        else:
            print(f"[VDataBProt] No data found for key: {key}")
            return None
    except Exception as e:
        print(f"ERROR: [VDataBProt] Failed to load data: {e}")
        return None
