import json

import pytest
from ex04_json_errors import LLMOutputError, extract_json, safe_get, to_json

FENCED_REPLY = """好的，以下是結果：
```json
{"supplier": "北辰五金", "total": 1200}
```
希望有幫助！"""


def test_extract_plain_json():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_from_json_fence():
    assert extract_json(FENCED_REPLY) == {"supplier": "北辰五金", "total": 1200}


def test_extract_from_plain_fence():
    assert extract_json('```\n{"x": [1, 2]}\n```') == {"x": [1, 2]}


def test_extract_from_surrounding_text():
    assert extract_json('Result: {"a": {"b": 1}} done.') == {"a": {"b": 1}}


def test_extract_fails_with_raw_text_and_cause():
    broken = "not json at all {broken"
    with pytest.raises(LLMOutputError) as exc_info:
        extract_json(broken)
    assert exc_info.value.raw == broken
    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)


def test_extract_rejects_non_object():
    with pytest.raises(LLMOutputError):
        extract_json("[1, 2, 3]")


def test_safe_get():
    data = {"a": {"b": {"c": 1}}, "items": [{"sku": "X"}], "n": None}
    assert safe_get(data, "a.b.c") == 1
    assert safe_get(data, "a.b") == {"c": 1}
    assert safe_get(data, "items.0.sku") == "X"


def test_safe_get_missing_returns_default():
    data = {"a": {"b": {"c": 1}}, "items": [{"sku": "X"}], "n": None}
    assert safe_get(data, "a.x.y", "N/A") == "N/A"
    assert safe_get(data, "items.5.sku") is None
    assert safe_get(data, "items.abc") is None
    assert safe_get(data, "n.foo", 0) == 0
    assert safe_get(data, "a.b.c.d") is None


def test_to_json():
    assert to_json({"b": 1, "a": "中文"}) == '{"a": "中文", "b": 1}'


def test_to_json_round_trip():
    data = {"supplier": "南星電子", "items": [{"sku": "A", "qty": 2}]}
    assert json.loads(to_json(data)) == data
