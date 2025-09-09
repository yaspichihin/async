#! /usr/bin/env python3
import asyncio
import logging

import aiohttp
from book_asyncio.utils import (
    async_timed,
    configure_logging,
    delay,
    fetch_status,
)

logger = logging.getLogger(__name__)


@async_timed()
async def main() -> None:
    delay_times = (5, 4, 3, 2, 1)
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    done, pending = await asyncio.wait(tasks)
    logger.debug("Завершенные задачи: %s", len(done))
    logger.debug("Оставшиеся задачи: %s", len(pending))

    for done_task in done:
        result = await done_task
        logger.debug("Результат: %s", result)

    async with aiohttp.ClientSession() as session:
        urls = ("https://ya.ru", "https://ya.ru")
        fetchers = [
            asyncio.create_task(fetch_status(session, url)) for url in urls
        ]
        done, pending = await asyncio.wait(fetchers)
        logger.debug("Завершенные задачи: %s", len(done))
        logger.debug("Оставшиеся задачи: %s", len(pending))
        for done_task in done:
            result = await done_task
            logger.debug("Результат: %s", result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
