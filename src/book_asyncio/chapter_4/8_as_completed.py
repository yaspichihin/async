#! /usr/bin/env python3
import asyncio
import logging

from book_asyncio.utils import async_timed, configure_logging, delay

logger = logging.getLogger(__name__)


@async_timed()
async def main() -> None:
    delay_times = (5, 4, 3, 2, 1)
    tasks = [delay(seconds) for seconds in delay_times]
    for task in asyncio.as_completed(tasks):
        result = await task
        logger.debug("Результат: %s", result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
