"""
挑戰題用的假 LLM —— 這個檔案不用改。

模擬真實 LLM API 會遇到的狀況：
- 每次呼叫要 0.2–0.8 秒
- 約 25% 機率丟出 RetryableError（像 503 / 429），重試通常就會好
- 回覆格式不一致：純 JSON、包在 ```json 裡、前後有廢話、數字變成字串
- 有幾份文件不管重試幾次，回來的內容都是壞的（輸出被截斷）
"""

import asyncio
import json
import random

from ex06_retry_decorator import RetryableError

DOC_IDS = [f"Q-{i:03d}" for i in range(1, 21)]

_SUPPLIERS = ["北辰五金", "南星電子", "西岳材料"]
_PRODUCTS = [
    ("M3-SCREW", "M3 螺絲"),
    ("CAP-10UF", "10uF 電容"),
    ("PCB-A1", "A1 電路板"),
    ("CBL-USB", "USB 線材"),
    ("BOX-S", "小紙箱"),
]


def _quote_for(doc_id: str) -> dict:
    rng = random.Random(doc_id)  # 同一份文件永遠產生同樣的內容
    items = [
        {
            "sku": sku,
            "description": desc,
            "qty": rng.randint(1, 200),
            "unit_price": round(rng.uniform(0.5, 300), 2),
        }
        for sku, desc in rng.sample(_PRODUCTS, k=rng.randint(1, 3))
    ]
    return {"supplier": rng.choice(_SUPPLIERS), "items": items}


def _render(doc_id: str, quote: dict) -> str:
    style = int(doc_id[-3:]) % 5
    body = json.dumps(quote, ensure_ascii=False, indent=2)
    if style == 0:
        return body
    if style == 1:
        return f"```json\n{body}\n```"
    if style == 2:
        return f"好的，以下是我從報價單整理出的結果：\n\n{body}\n\n如果需要調整請告訴我！"
    if style == 3:
        for item in quote["items"]:
            item["qty"] = str(item["qty"])
            item["unit_price"] = str(item["unit_price"])
        return f"```\n{json.dumps(quote, ensure_ascii=False)}\n```"
    return body[: len(body) // 2] + "\n...（輸出長度超過上限，已截斷）"


async def fake_llm(doc_id: str) -> str:
    """假裝把報價單 doc_id 丟給 LLM 抽取，回傳模型的原始文字回覆。"""
    await asyncio.sleep(random.uniform(0.2, 0.8))
    if random.random() < 0.25:
        raise RetryableError(f"503 Service Unavailable ({doc_id})")
    return _render(doc_id, _quote_for(doc_id))


if __name__ == "__main__":
    # 直接執行這個檔案可以看看 LLM 回什麼：uv run python 01-python-for-ts-devs/fake_llm.py
    for doc_id in DOC_IDS[:5]:
        print(f"===== {doc_id} =====")
        print(_render(doc_id, _quote_for(doc_id)))
        print()
