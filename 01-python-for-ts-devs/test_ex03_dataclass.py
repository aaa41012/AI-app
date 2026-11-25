import pytest
from ex03_dataclass import LineItem, Quote, Status


def test_status_values():
    assert Status.PENDING == "pending"
    assert Status("approved") is Status.APPROVED
    assert {s.value for s in Status} == {"pending", "approved", "rejected"}


def test_line_item_fields_and_subtotal():
    item = LineItem("A-100", 3, 2.5)
    assert item.sku == "A-100"
    assert item.qty == 3
    assert item.description == ""
    assert item.subtotal == 7.5


def test_line_item_equality():
    # dataclass 自動產生 __eq__：欄位都相同就相等（JS 的物件比較是比 reference）
    assert LineItem("A", 1, 1.0) == LineItem("A", 1, 1.0)
    assert LineItem("A", 1, 1.0) != LineItem("A", 2, 1.0)


def test_quote_defaults():
    q = Quote(supplier="北辰五金")
    assert q.items == []
    assert q.status is Status.PENDING


def test_quote_items_not_shared_between_instances():
    a = Quote(supplier="A")
    b = Quote(supplier="B")
    a.add_item(LineItem("X", 1, 1.0))
    assert b.items == []


def test_quote_total():
    q = Quote(supplier="北辰五金")
    q.add_item(LineItem("A", 2, 10.0))
    q.add_item(LineItem("B", 3, 1.5))
    assert q.total() == 24.5


def test_approve_only_from_pending():
    q = Quote(supplier="X")
    q.approve()
    assert q.status is Status.APPROVED
    with pytest.raises(ValueError):
        q.approve()
    with pytest.raises(ValueError):
        q.reject()


def test_reject_only_from_pending():
    q = Quote(supplier="X")
    q.reject()
    assert q.status is Status.REJECTED
    with pytest.raises(ValueError):
        q.approve()


def test_from_dict_converts_types():
    q = Quote.from_dict(
        {
            "supplier": "北辰五金",
            "items": [
                {"sku": "A-1", "qty": "2", "unit_price": "10"},
                {"sku": "B-2", "qty": 1, "unit_price": 5.5, "description": "電容"},
            ],
        }
    )
    assert q == Quote(
        supplier="北辰五金",
        items=[LineItem("A-1", 2, 10.0), LineItem("B-2", 1, 5.5, "電容")],
    )
    assert isinstance(q.items[0].qty, int)
    assert isinstance(q.items[0].unit_price, float)


def test_from_dict_defaults():
    q = Quote.from_dict({"supplier": "X"})
    assert q.items == []
    assert q.status is Status.PENDING


def test_from_dict_with_status():
    assert Quote.from_dict({"supplier": "X", "status": "approved"}).status is Status.APPROVED
    with pytest.raises(ValueError):
        Quote.from_dict({"supplier": "X", "status": "whatever"})
