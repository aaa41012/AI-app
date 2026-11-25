"""
Ex01 — 基本語法：字串、f-string、函式、keyword-only 參數、None

TS 對照：
  const x = 1 / let x = 1   → x = 1（沒有宣告關鍵字）
  `${a} ${b}`               → f"{a} {b}"
  null / undefined          → None
  ===                       → ==（判斷 None 要用 x is None）
  &&  ||  !                 → and  or  not
  s.trim()                  → s.strip()
  s.toUpperCase()           → s.upper()
  arr.join("")              → "".join(arr)

執行測試：uv run pytest 01-python-for-ts-devs/test_ex01_basics.py
"""


def normalize_sku(raw: str) -> str:
    """把使用者或 LLM 給的料號正規化。

    規則：去頭尾空白 → 轉大寫 → 移除中間所有空白

      normalize_sku("  ab-12 34 ") == "AB-1234"
      normalize_sku("x 1") == "X1"

    提示：s.split() 不帶參數會用「任意空白」切開
    """
    raise NotImplementedError


def format_price(amount: float, currency: str = "TWD") -> str:
    """格式化金額：千分位 + 兩位小數。

      format_price(1234.5) == "TWD 1,234.50"
      format_price(0.1, "USD") == "USD 0.10"

    提示：f-string 的格式化語法 f"{x:,.2f}"（≈ toLocaleString + toFixed(2)）
    """
    raise NotImplementedError


def parse_quantity(text: str) -> int | None:
    r"""從 "12 pcs"、"數量: 30 個"、"  7件" 這類文字取出第一個整數；找不到回傳 None。

      parse_quantity("12 pcs") == 12
      parse_quantity("數量: 30 個") == 30
      parse_quantity("abc") is None

    提示：import re
          m = re.search(r"\d+", text)   # 找不到回傳 None（像 JS 的 match 回 null）
          m.group()                     # 取出比對到的字串
    注意：回傳的要是 int，不是 str
    """
    raise NotImplementedError


def describe_item(name: str, qty: int, *, unit: str = "pcs", note: str | None = None) -> str:
    """組出一行品項描述。

    參數列裡的 `*` 代表：後面的參數只能用關鍵字傳（keyword-only），
    呼叫時一定要寫 unit="盒"，不能寫 describe_item("螺絲", 10, "盒")。
    這就是 Python 版的 TS options 物件：f(name, qty, { unit, note })

      describe_item("螺絲", 10) == "螺絲 x10 pcs"
      describe_item("螺絲", 10, unit="盒") == "螺絲 x10 盒"
      describe_item("螺絲", 10, note="急件") == "螺絲 x10 pcs (急件)"
    """
    raise NotImplementedError
