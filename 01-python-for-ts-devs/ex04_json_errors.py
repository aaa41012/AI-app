"""
Ex04 — JSON 與例外處理：解析「不聽話」的 LLM 輸出

TS 對照：
  JSON.parse(s)                  → json.loads(s)
  JSON.stringify(obj)            → json.dumps(obj, ensure_ascii=False)
  try {} catch (e) {}            → try: ... except SomeError as e: ...
  throw new Error("x")           → raise ValueError("x")
  class MyError extends Error {} → class MyError(Exception): ...
  new Error("x", { cause: e })   → raise MyError("x") from e

就算你叫 LLM「只回 JSON」，它還是很常回這種東西：

  好的，以下是結果：
  ```json
  {"supplier": "北辰五金", "total": 1200}
  ```
  希望有幫助！

Stage 3 會用 structured outputs 從根本避免這件事，但你仍然要會處理 ——
不是每個模型都支援（地端模型特別常見），而且輸出還可能被截斷。
"""

import json  # noqa: F401  ← 實作時會用到
from typing import Any


class LLMOutputError(Exception):
    """LLM 輸出無法解析時丟出。保留原始文字，之後除錯、記 log 都需要它。"""

    def __init__(self, message: str, raw: str):
        super().__init__(message)
        self.raw = raw


def extract_json(text: str) -> dict:
    """從 LLM 的回覆中取出 JSON 物件。

    依序嘗試，第一個成功的就回傳：
      1. 整段文字直接 json.loads
      2. 取 ```json ... ``` 或 ``` ... ``` code fence 裡面的內容
      3. 取第一個 "{" 到最後一個 "}" 之間的內容

    - 解析出來不是 dict（例如是 list）也算失敗
    - 全部失敗 → raise LLMOutputError(訊息, raw=原始文字)，
      並用 `raise ... from 最後一個錯誤` 把原本的 JSONDecodeError 串起來

    提示：import re
          re.search(r"```(?:json)?\\s*(.*?)```", text, re.DOTALL)
          （re.DOTALL 讓 . 也能比對換行）
    """
    raise NotImplementedError


def safe_get(data: dict, path: str, default: Any = None) -> Any:
    """用點號路徑取巢狀的值（≈ lodash.get，或 JS 的 data?.a?.b?.c ?? default）。

      safe_get({"a": {"b": {"c": 1}}}, "a.b.c") == 1
      safe_get({"a": {"b": 1}}, "a.x.y", "N/A") == "N/A"
      safe_get({"items": [{"sku": "X"}]}, "items.0.sku") == "X"   ← 遇到 list 時，key 當 index 用

    任何一層不存在、型別不對、index 超出範圍 → 回傳 default，不能讓例外漏出去。
    """
    raise NotImplementedError


def to_json(data: dict) -> str:
    """轉成 JSON 字串：中文不要變成 \\uXXXX、key 要排序。

      to_json({"b": 1, "a": "中文"}) == '{"a": "中文", "b": 1}'

    為什麼要排序？輸出穩定（同樣的資料永遠產生同樣的字串），
    之後做快取、比對、prompt caching 都靠這個。
    """
    raise NotImplementedError
