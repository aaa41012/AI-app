import copy

import pytest
from ex02_collections import chunk_text, group_by_supplier, skus_over, top_n_expensive, total_amount

ITEMS = [
    {"sku": "A-100", "supplier": "北辰五金", "qty": 10, "unit_price": 25.0},  # 小計 250
    {"sku": "B-200", "supplier": "南星電子", "qty": 2, "unit_price": 300.0},  # 小計 600
    {"sku": "C-300", "supplier": "北辰五金", "qty": 100, "unit_price": 1.5},  # 小計 150
    {"sku": "D-400", "supplier": "西岳材料", "qty": 1, "unit_price": 999.0},  # 小計 999
]


def test_total_amount():
    assert total_amount(ITEMS) == 1999.0
    assert total_amount([]) == 0


def test_skus_over():
    assert skus_over(ITEMS, 25.0) == ["A-100", "B-200", "D-400"]
    assert skus_over(ITEMS, 10_000) == []


def test_group_by_supplier():
    groups = group_by_supplier(ITEMS)
    assert set(groups) == {"北辰五金", "南星電子", "西岳材料"}
    assert [i["sku"] for i in groups["北辰五金"]] == ["A-100", "C-300"]
    assert [i["sku"] for i in groups["西岳材料"]] == ["D-400"]


def test_top_n_expensive():
    top = top_n_expensive(ITEMS, 2)
    assert [i["sku"] for i in top] == ["D-400", "B-200"]


def test_top_n_expensive_does_not_mutate_input():
    items = copy.deepcopy(ITEMS)
    top_n_expensive(items, 2)
    assert items == ITEMS


def test_chunk_text_examples():
    assert chunk_text("abcdefghij", 4, 1) == ["abcd", "defg", "ghij"]
    assert chunk_text("abcdefgh", 4, 1) == ["abcd", "defg", "gh"]
    assert chunk_text("abc", 5, 2) == ["abc"]
    assert chunk_text("abcdefg", 4, 1) == ["abcd", "defg"]


def test_chunk_text_empty():
    assert chunk_text("", 10, 2) == []


def test_chunk_text_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("abc", 4, 4)
    with pytest.raises(ValueError):
        chunk_text("abc", 4, -1)


def test_chunk_text_can_be_reassembled():
    """把每段去掉重疊的部分接起來，應該等於原文 —— 代表沒有漏字也沒有多字"""
    text = "".join(chr(ord("a") + i % 26) for i in range(100))
    chunks = chunk_text(text, size=20, overlap=5)
    assert all(len(c) <= 20 for c in chunks)
    assert chunks[0] + "".join(c[5:] for c in chunks[1:]) == text
