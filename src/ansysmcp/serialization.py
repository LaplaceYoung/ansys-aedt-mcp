from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

MAX_SEQUENCE_ITEMS = 100
MAX_MAPPING_ITEMS = 100


def to_jsonable(value: Any, *, depth: int = 0, max_depth: int = 5) -> Any:
    """Convert PyAEDT, COM, and common Python objects into MCP-safe data."""
    if depth > max_depth:
        return {"type": type(value).__name__, "repr": safe_repr(value)}

    if value is None or isinstance(value, str | int | float | bool):
        return value

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, Mapping):
        return {
            str(key): to_jsonable(item, depth=depth + 1, max_depth=max_depth)
            for key, item in list(value.items())[:MAX_MAPPING_ITEMS]
        }

    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [
            to_jsonable(item, depth=depth + 1, max_depth=max_depth)
            for item in list(value)[:MAX_SEQUENCE_ITEMS]
        ]

    if hasattr(value, "model_dump"):
        try:
            return to_jsonable(value.model_dump(), depth=depth + 1, max_depth=max_depth)
        except Exception:
            pass

    if hasattr(value, "__dict__") and depth < max_depth:
        summary = summarize_object(value)
        public_data = {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_") and isinstance(item, str | int | float | bool | type(None))
        }
        if public_data:
            summary["attributes"] = public_data
        return summary

    return summarize_object(value)


def summarize_object(value: Any) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "type": f"{type(value).__module__}.{type(value).__name__}",
        "repr": safe_repr(value),
    }
    for attr in ("name", "id", "object_id", "material_name", "solution_type"):
        if hasattr(value, attr):
            try:
                attr_value = getattr(value, attr)
            except Exception:
                continue
            if not callable(attr_value):
                summary[attr] = attr_value
    return summary


def safe_repr(value: Any) -> str:
    try:
        text = repr(value)
    except Exception:
        text = f"<{type(value).__name__}>"
    if len(text) > 500:
        return text[:497] + "..."
    return text
