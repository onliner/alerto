from typing import Final, Optional, Callable, Awaitable

import asyncio
from pyrate_limiter import Limiter, Duration, Rate, InMemoryBucket

from src.settings import settings

RATES: Final = [Rate(settings.messages_per_minute, Duration.MINUTE)]
FlushTask = Optional[asyncio.Task]
FlushCallback = Callable[[int], Awaitable[None]]


class RateLimiter:
    def __init__(self) -> None:
        self._delay = settings.max_delay
        self._failed_attempts: int = 0
        self._flush_task: FlushTask = None

        self.limiter = Limiter(
            InMemoryBucket(RATES),
            raise_when_fail=False,
            retry_until_max_delay=True,
            max_delay=self._delay,
        )

    def try_acquire(self, *, weight: int = 1) -> bool:
        if self.limiter.try_acquire(settings.chat_id, weight=weight):
            return True

        self._failed_attempts += 1
        return False

    def schedule_flush(self, callback: FlushCallback) -> None:
        if self._flush_task is None or self._flush_task.done():
            self._flush_task = asyncio.create_task(
                self._flush_when_available(callback)
            )

    async def _flush_when_available(self, callback: FlushCallback) -> None:
        while self._failed_attempts > 0:
            if self.try_acquire():
                count = self._failed_attempts
                self._failed_attempts = 0
                await callback(count)
                return
            await asyncio.sleep(self._delay / 1000)


limiter = RateLimiter()
