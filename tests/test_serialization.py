from __future__ import annotations

from ansysmcp.serialization import to_jsonable


class ObjectWithName:
    name = "Box1"


def test_to_jsonable_converts_nested_data() -> None:
    data = {"items": [1, "x", {"y": True}]}
    assert to_jsonable(data) == data


def test_to_jsonable_summarizes_unknown_object() -> None:
    result = to_jsonable(ObjectWithName())
    assert result["name"] == "Box1"
    assert result["type"].endswith("ObjectWithName")
