import asyncio

import pytest
from ex06_retry_decorator import FatalError, RetryableError, retry


@pytest.fixture
def sleeps(monkeypatch):
    """攔截 asyncio.sleep：不真的等，只記錄每次等了幾秒（≈ jest.useFakeTimers）"""
    recorded: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        recorded.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    return recorded


def test_success_on_first_try(sleeps):
    calls = 0

    @retry(max_attempts=3, base_delay=1)
    async def ok():
        nonlocal calls
        calls += 1
        return "done"

    assert asyncio.run(ok()) == "done"
    assert calls == 1
    assert sleeps == []


def test_retries_then_succeeds(sleeps):
    calls = 0

    @retry(max_attempts=3, base_delay=1)
    async def flaky():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RetryableError("503")
        return "ok"

    assert asyncio.run(flaky()) == "ok"
    assert calls == 3
    assert sleeps == [1, 2], "指數退避：第 1 次失敗等 1 秒，第 2 次失敗等 2 秒"


def test_gives_up_after_max_attempts(sleeps):
    calls = 0

    @retry(max_attempts=4, base_delay=0.5)
    async def always_fail():
        nonlocal calls
        calls += 1
        raise RetryableError(f"fail #{calls}")

    with pytest.raises(RetryableError, match="fail #4"):
        asyncio.run(always_fail())
    assert calls == 4
    assert sleeps == [0.5, 1.0, 2.0], "最後一次失敗後不用再等"


def test_does_not_retry_other_errors(sleeps):
    calls = 0

    @retry(max_attempts=5, base_delay=1)
    async def bad_request():
        nonlocal calls
        calls += 1
        raise FatalError("400 Bad Request")

    with pytest.raises(FatalError):
        asyncio.run(bad_request())
    assert calls == 1
    assert sleeps == []


def test_custom_retry_on(sleeps):
    calls = 0

    @retry(max_attempts=2, base_delay=1, retry_on=(TimeoutError,))
    async def slow():
        nonlocal calls
        calls += 1
        raise TimeoutError()

    with pytest.raises(TimeoutError):
        asyncio.run(slow())
    assert calls == 2


def test_passes_arguments_through(sleeps):
    @retry()
    async def add(a, b, *, c=0):
        return a + b + c

    assert asyncio.run(add(1, 2, c=3)) == 6


def test_preserves_function_name():
    @retry()
    async def call_erp():
        return None

    assert call_erp.__name__ == "call_erp"
