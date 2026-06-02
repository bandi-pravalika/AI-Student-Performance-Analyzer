"""Helper utilities."""
import json
from pathlib import Path
from typing import Any, Dict


def save_json(data: Dict[str, Any], filepath: str):
    """Save dictionary to JSON file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def load_json(filepath: str) -> Dict[str, Any]:
    """Load dictionary from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format number as percentage."""
    return f"{value:.{decimals}f}%"


def format_score(score: float, decimals: int = 2) -> str:
    """Format score with decimals."""
    return f"{score:.{decimals}f}"
