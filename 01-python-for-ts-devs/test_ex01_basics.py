import pytest
from ex01_basics import describe_item, format_price, normalize_sku, parse_quantity


def test_normalize_sku():
    assert normalize_sku("  ab-12 34 ") == "AB-1234"
    assert normalize_sku("x 1") == "X1"
    assert normalize_sku("ABC") == "ABC"


def test_format_price_default_currency():
    assert format_price(1234.5) == "TWD 1,234.50"
    assert format_price(1_000_000) == "TWD 1,000,000.00"


def test_format_price_custom_currency():
    assert format_price(0.1, "USD") == "USD 0.10"


def test_parse_quantity():
    assert parse_quantity("12 pcs") == 12
    assert parse_quantity("數量: 30 個") == 30
    assert parse_quantity("  7件") == 7


def test_parse_quantity_returns_int():
    assert isinstance(parse_quantity("5"), int)


def test_parse_quantity_not_found():
    assert parse_quantity("abc") is None
    assert parse_quantity("") is None


def test_describe_item():
    assert describe_item("螺絲", 10) == "螺絲 x10 pcs"
    assert describe_item("螺絲", 10, unit="盒") == "螺絲 x10 盒"
    assert describe_item("螺絲", 10, note="急件") == "螺絲 x10 pcs (急件)"
    assert describe_item("螺絲", 10, unit="盒", note="急件") == "螺絲 x10 盒 (急件)"


def test_describe_item_unit_is_keyword_only():
    with pytest.raises(TypeError):
        describe_item("螺絲", 10, "盒")  # type: ignore[misc]
