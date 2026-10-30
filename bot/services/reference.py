"""Reference book service — lookup deadline rules by keyword."""
import json
import os

# Load reference data
REF_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'reference.json')

with open(REF_PATH, 'r', encoding='utf-8') as f:
    _ref_data = json.load(f)


def get_version() -> str:
    """Get reference version."""
    return _ref_data.get('version', 'unknown')


def search(query: str) -> list[dict]:
    """Search reference by keyword.

    Matches against action, law, and deadline fields.
    """
    query_lower = query.lower()
    results = []

    for item in _ref_data['items']:
        # Check action
        if query_lower in item['action'].lower():
            results.append(item)
            continue

        # Check law
        if query_lower in item['law'].lower():
            results.append(item)
            continue

        # Check deadline
        if query_lower in item['deadline'].lower():
            results.append(item)
            continue

        # Check from field
        if query_lower in item['from'].lower():
            results.append(item)
            continue

    return results


def get_item(item_id: str) -> dict | None:
    """Get a specific reference item by ID."""
    for item in _ref_data['items']:
        if item['id'] == item_id:
            return item
    return None