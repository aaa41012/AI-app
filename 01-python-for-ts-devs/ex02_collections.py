"""
Ex02 — list / dict / 推導式（comprehension）/ 排序 / slicing

TS 對照：
  arr.map(x => x * 2)              → [x * 2 for x in arr]
  arr.filter(x => x > 0)           → [x for x in arr if x > 0]
  arr.reduce((a, b) => a + b, 0)   → sum(arr)
  arr.length                       → len(arr)
  obj.key ?? "預設"                 → obj.get("key", "預設")
  arr.toSorted((a, b) => b.n - a.n) → sorted(arr, key=lambda x: x["n"], reverse=True)
  arr.slice(0, 3)                  → arr[:3]

這份練習的資料長這樣（像 LLM 從報價單抽出來的 line items）：
  {"sku": "A-100", "supplier": "北辰五金", "qty": 10, "unit_price": 25.0}
"""


def total_amount(items: list[dict]) -> float:
    """所有品項 qty * unit_price 的總和。空 list 回傳 0。

    挑戰：用一行寫完（sum + generator expression）
    """
    raise NotImplementedError


def skus_over(items: list[dict], min_price: float) -> list[str]:
    """unit_price >= min_price 的 sku 清單，保持原本順序。用 list comprehension 一行寫完。"""
    raise NotImplementedError


def group_by_supplier(items: list[dict]) -> dict[str, list[dict]]:
    """依 supplier 分組（≈ lodash 的 groupBy / Object.groupBy）。

    提示：兩種寫法都試試看
      1. result.setdefault(key, []).append(item)
      2. from collections import defaultdict
    """
    raise NotImplementedError


def top_n_expensive(items: list[dict], n: int) -> list[dict]:
    """依小計（qty * unit_price）由大到小，取前 n 筆。不能改動傳進來的 list。

    提示：sorted() 回傳新 list；list.sort() 會原地修改（跟 JS 的 arr.sort() 一樣）
    """
    raise NotImplementedError


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """把長文字切成有重疊的片段 —— 這就是 RAG chunking 最基本的版本（Stage 4 會再升級）。

    規則：
    - 每段最多 size 個字元
    - 下一段的起點 = 上一段的起點 + (size - overlap)
    - 某一段已經涵蓋到文字結尾，就停止
    - text 是空字串時回傳 []
    - overlap < 0 或 overlap >= size 時 raise ValueError

      chunk_text("abcdefghij", 4, 1) == ["abcd", "defg", "ghij"]
      chunk_text("abcdefgh", 4, 1)   == ["abcd", "defg", "gh"]
      chunk_text("abc", 5, 2)        == ["abc"]

    提示：text[i:i + size] 超出範圍不會報錯（跟 JS 的 slice 一樣）
          range(start, stop, step) 可以指定步長
    """
    raise NotImplementedError
