"""
Ex05 — async / await：同時呼叫多個 API

TS 對照：
  async function f() {}             → async def f(): ...
  await p                           → await coro
  Promise.all([a, b])               → await asyncio.gather(a, b)
  Promise.allSettled([a, b])        → await asyncio.gather(a, b, return_exceptions=True)
  Promise.race([p, timeout(1000)])  → await asyncio.wait_for(coro, timeout=1)
  p-limit(3)                        → asyncio.Semaphore(3)
  await new Promise(r => setTimeout(r, 1000)) → await asyncio.sleep(1)
  function f<T>(x: T): T            → def f[T](x: T) -> T:

⚠️ 跟 JS 最大的差別：
  JS 呼叫 async function，它就「開始跑」了。
  Python 呼叫 async def 只會得到一個 coroutine 物件，什麼都還沒發生 ——
  要 await 它，或交給 asyncio.gather / asyncio.create_task 才會執行。

為什麼重要：一次 LLM 呼叫要 2–30 秒。處理 50 份報價單時，
「同時跑、但限制併發數量（避免撞到 rate limit）」是每天都會寫的東西。
"""

import asyncio  # noqa: F401  ← 實作時會用到
from collections.abc import Awaitable, Callable


async def fetch_all[T](ids: list[str], fetch: Callable[[str], Awaitable[T]]) -> list[T]:
    """對每個 id 呼叫 fetch(id)，全部「同時」執行，回傳結果（順序要跟 ids 一致）。

    提示：asyncio.gather(*[...]) —— 注意 * 是把 list 展開成多個參數（≈ JS 的 ...arr）
    """
    raise NotImplementedError


async def fetch_with_timeout[T](coro: Awaitable[T], seconds: float) -> T | None:
    """超過 seconds 秒就放棄並回傳 None；沒超時就回傳結果。

    提示：asyncio.wait_for(...)，超時會丟 TimeoutError
    """
    raise NotImplementedError


async def fetch_all_limited[T](
    ids: list[str], fetch: Callable[[str], Awaitable[T]], limit: int
) -> list[T]:
    """跟 fetch_all 一樣，但同一時間最多只有 limit 個 fetch 在跑。

    提示：
      sem = asyncio.Semaphore(limit)

      async def worker(id):
          async with sem:          # 拿不到名額就在這裡等
              return await fetch(id)
    """
    raise NotImplementedError


async def fetch_all_settled[T](
    ids: list[str], fetch: Callable[[str], Awaitable[T]]
) -> tuple[list[T], list[str]]:
    """≈ Promise.allSettled：全部跑完，不會因為其中一個失敗就整批中斷。

    回傳 (成功的結果 list, 失敗的 id list)，兩者都保持原本順序。
    Python 可以直接回傳 tuple，呼叫端用 ok, failed = await ... 解構。

    提示：gather(..., return_exceptions=True) 會把例外當成結果放進 list，
          再用 isinstance(r, Exception) 分類；zip(ids, results) 可以把兩個 list 配對
    """
    raise NotImplementedError
