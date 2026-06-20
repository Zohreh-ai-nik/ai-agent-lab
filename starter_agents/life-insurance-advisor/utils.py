# utils.py
# PURPOSE: Helper functions used across the app
import json
from typing import Any, Dict, Optional


def format_currency(amount: float, currency_code: str) -> str:
    """Converts a number to currency string e.g. 813574 → $813,574"""
    symbol_map = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "CAD": "C$",
        "AUD": "A$",
        "INR": "₹",
    }
    code = (currency_code or "USD").upper()
    symbol = symbol_map.get(code, "")
    formatted = f"{amount:,.0f}"
    return f"{symbol}{formatted}" if symbol else f"{formatted} {code}"


def extract_json(payload: str) -> Optional[Dict[str, Any]]:
    """
    Extracts JSON from agent response.
    Agent sometimes wraps JSON in ```json ... ``` markdown blocks.
    This function handles both cases.
    """
    if not payload:
        return None

    content = payload.strip()

    # Remove markdown code block if present
    if content.startswith("```"):
        lines = content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def parse_percentage(value: Any, fallback: float = 0.02) -> float:
    """
    Converts percentage values to decimal.
    Examples:
        "2%"  → 0.02
        2     → 0.02
        0.02  → 0.02
    """
    if value is None:
        return fallback
    if isinstance(value, (int, float)):
        return float(value) if value < 1 else float(value) / 100
    if isinstance(value, str):
        cleaned = value.strip().replace("%", "")
        try:
            numeric = float(cleaned)
            return numeric if numeric < 1 else numeric / 100
        except ValueError:
            return fallback
    return fallback