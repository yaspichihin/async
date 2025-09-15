#! /usr/bin/env python3
import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter += 1
    return counter


async def main():
    # Создал пул процессов
    with ProcessPoolExecutor() as pool:
        # Получил цикл событий
        loop = asyncio.get_event_loop()
        numbers = list(range(10))

        # Создал список вызовов ("частичное применение")
        # partial(count, num): создаёт вызываемый объект,
        # у которого аргумент count_to зафиксирован значением num.
        calls = [partial(count, num) for num in numbers]

        # Запустил вызовы в пуле процессов
        call_coros = [loop.run_in_executor(pool, call) for call in calls]

        # Получил результаты, можно использовать asyncio.as_completed
        results = await asyncio.gather(*call_coros)
        for result in results:
            logger.debug(result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
