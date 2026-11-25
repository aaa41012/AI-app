"""
Ex03 — 型別：dataclass、Enum、@property、@classmethod

TS 對照：
  interface / class 只放資料      → @dataclass（自動產生 __init__、__eq__、__repr__）
  enum Status { Pending = "pending" } → class Status(StrEnum): PENDING = "pending"
  get subtotal() { ... }          → @property
  static fromJSON(data) { ... }   → @classmethod def from_dict(cls, data)
  this                            → self（要明確寫在方法的第一個參數）
  回傳型別 this                    → Self（from typing import Self）

⚠️ 經典陷阱：可變的預設值
  在 dataclass 裡寫 items: list = []，Python 會直接報錯提醒你，要改成
  items: list[X] = field(default_factory=list)
  但一般函式寫 def f(items=[]) 不會報錯，而是「每次呼叫共用同一個 list」——
  這是 JS 沒有的坑（ruff 的 B006 規則會幫你抓）。

Stage 2 的 Pydantic 會取代這裡大部分手工轉換，但概念一模一樣。
"""

from dataclasses import dataclass, field  # noqa: F401  ← 實作時會用到 field，做完可以刪掉這個 noqa
from enum import StrEnum
from typing import Self


class Status(StrEnum):
    # TODO: 三個狀態
    #   PENDING = "pending"
    #   APPROVED = "approved"
    #   REJECTED = "rejected"
    pass


@dataclass
class LineItem:
    # TODO: 定義欄位（順序很重要，測試會用位置參數建立 LineItem("A-1", 3, 2.5)）
    #   sku: str
    #   qty: int
    #   unit_price: float
    #   description: str，預設 ""

    @property
    def subtotal(self) -> float:
        """qty * unit_price"""
        raise NotImplementedError


@dataclass
class Quote:
    # TODO: 定義欄位
    #   supplier: str
    #   items: list[LineItem]，預設空 list（記得用 field(default_factory=...)）
    #   status: Status，預設 Status.PENDING

    def add_item(self, item: LineItem) -> None:
        raise NotImplementedError

    def total(self) -> float:
        """所有 item 的 subtotal 加總"""
        raise NotImplementedError

    def approve(self) -> None:
        """只有 PENDING 可以核准，其他狀態 raise ValueError。（HITL 審核狀態機的雛形）"""
        raise NotImplementedError

    def reject(self) -> None:
        """只有 PENDING 可以駁回，其他狀態 raise ValueError。"""
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """從 dict（例如 LLM 回傳的 JSON）建立 Quote。

          {"supplier": "北辰五金", "items": [{"sku": "A-1", "qty": "2", "unit_price": "10"}]}

        - 沒有 items 時視為空 list
        - 沒有 description 時為 ""
        - 沒有 status 時為 PENDING；有的話用 Status(data["status"]) 轉換（不合法的值會自己丟 ValueError）
        - qty 轉成 int、unit_price 轉成 float —— LLM 很常把數字回成字串 "10"
        """
        raise NotImplementedError
