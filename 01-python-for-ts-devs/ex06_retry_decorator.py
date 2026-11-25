"""
Ex06 — Decorator + Retry：讓不穩的 API 自動重試

decorator 本質上就是 higher-order function。TS 的寫法：

  const withLog = (fn) => (...args) => { console.log("call"); return fn(...args) }
  const myFunc = withLog(originalFunc)

Python：

  def with_log(fn):
      def wrapper(*args, **kwargs):
          print("call")
          return fn(*args, **kwargs)
      return wrapper

  @with_log            ← 語法糖，等於 my_func = with_log(my_func)
  def my_func(): ...

帶參數的 decorator 要多包一層：@retry(max_attempts=3) 先呼叫 retry(3)，
回傳一個 decorator，再拿那個 decorator 去包函式。所以是三層：

  def retry(max_attempts):        ← 接設定
      def decorator(fn):          ← 接被包的函式
          async def wrapper(*args, **kwargs):   ← 實際被呼叫的東西
              ...
          return wrapper
      return decorator

串接不穩定的第三方 API（LLM、ERP）時，retry 是一定要有的防線。
實務上會用 tenacity 套件（Stage 7），但自己寫過一次，才知道它在幫你做什麼。
"""

import asyncio  # noqa: F401  ← 實作時會用到
import functools  # noqa: F401  ← 實作時會用到


class RetryableError(Exception):
    """可以重試的錯誤，例如 429 Too Many Requests、503、timeout"""


class FatalError(Exception):
    """不該重試的錯誤，例如 400 參數錯誤、401 沒有權限 —— 重試幾次都一樣會失敗"""


def retry(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    retry_on: tuple[type[Exception], ...] = (RetryableError,),
):
    """給 async 函式用的重試 decorator，指數退避（exponential backoff）。

    - max_attempts 是「總共最多試幾次」（包含第一次）
    - 第 1 次失敗後等 base_delay 秒，第 2 次失敗後等 base_delay * 2，再來 * 4、* 8 …
    - 最後一次失敗後不用再等，直接把那個例外往外丟
    - 只有 retry_on 裡的例外才重試；其他例外直接往外丟，不重試
    - 等待一定要用 `await asyncio.sleep(...)`（測試會攔截它來檢查你等了幾秒）
    - 用 @functools.wraps(fn) 保留原函式的名稱（否則所有被包的函式都會叫 "wrapper"）

    使用方式：

        @retry(max_attempts=3, base_delay=0.1)
        async def call_erp(order_id: str) -> dict: ...

    進階（選做）：真實世界會加 jitter（隨機抖動），避免一堆 client 同時重試又同時撞上去。
    """

    def decorator(fn):
        raise NotImplementedError

    return decorator
