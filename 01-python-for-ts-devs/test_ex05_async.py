import asyncio
import time

from ex05_async import fetch_all, fetch_all_limited, fetch_all_settled, fetch_with_timeout


async def slow_upper(x: str, delay: float = 0.2) -> str:
    await asyncio.sleep(delay)
    return x.upper()


def test_fetch_all_runs_concurrently():
    start = time.perf_counter()
    result = asyncio.run(fetch_all(["a", "b", "c", "d", "e"], slow_upper))
    elapsed = time.perf_counter() - start
    assert result == ["A", "B", "C", "D", "E"]
    assert elapsed < 0.5, (
        f"花了 {elapsed:.2f} 秒 —— 一個一個 await 的話要 1 秒，你是不是沒有同時跑？"
    )


def test_fetch_all_keeps_order():
    async def later_ones_finish_first(x: str) -> int:
        await asyncio.sleep(0.05 * (3 - int(x)))
        return int(x)

    assert asyncio.run(fetch_all(["0", "1", "2"], later_ones_finish_first)) == [0, 1, 2]


def test_fetch_with_timeout_returns_result():
    assert asyncio.run(fetch_with_timeout(slow_upper("x", 0.01), 1)) == "X"


def test_fetch_with_timeout_returns_none():
    start = time.perf_counter()
    assert asyncio.run(fetch_with_timeout(slow_upper("x", 2), 0.05)) is None
    assert time.perf_counter() - start < 1, "超時後應該馬上放棄，不是等它跑完"


def test_fetch_all_limited_respects_limit():
    running = 0
    peak = 0

    async def tracked(x: str) -> str:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.05)
        running -= 1
        return x

    ids = [str(i) for i in range(10)]
    result = asyncio.run(fetch_all_limited(ids, tracked, limit=3))
    assert result == ids
    assert peak == 3, f"同時最多跑了 {peak} 個，應該要剛好 3 個"


def test_fetch_all_settled():
    async def flaky(x: str) -> str:
        await asyncio.sleep(0.01)
        if x.startswith("bad"):
            raise RuntimeError(f"{x} 壞掉了")
        return x.upper()

    ok, failed = asyncio.run(fetch_all_settled(["a", "bad1", "b", "bad2"], flaky))
    assert ok == ["A", "B"]
    assert failed == ["bad1", "bad2"]
