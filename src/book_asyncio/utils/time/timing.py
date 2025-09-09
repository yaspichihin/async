import asyncio
import functools
import logging
import time
from collections.abc import Callable
from typing import Any


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            logger = logging.getLogger(__name__)
            logger.debug(
                "Выполняется %s с аргументами %s %s",
                func.__name__,
                args,
                kwargs,
            )
            start = time.perf_counter_ns()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.perf_counter_ns()
                total = (end - start) * 1e-9
                logger.debug(
                    "Функция %s завершилась за %.4f с",
                    func.__name__,
                    total,
                )

        return wrapped

    return wrapper


async def delay(delay_seconds: int) -> int:
    logger = logging.getLogger(__name__)
    logger.debug("Засыпаю на %s секунд", delay_seconds)
    await asyncio.sleep(delay_seconds)
    logger.debug("Просыпаюсь после задержки: %s секунд", delay_seconds)
    return delay_seconds
