#! /usr/bin/env python3
import asyncio
import logging

import aiohttp
from book_asyncio.utils import async_timed, configure_logging, fetch_status

logger = logging.getLogger(__name__)


@async_timed()
async def main() -> None:
    async with aiohttp.ClientSession() as session:
        pending_tasks = [
            asyncio.create_task(fetch_status(session, "https://ya.ru")),
            asyncio.create_task(fetch_status(session, "https://mail.ru")),
            asyncio.create_task(
                fetch_status(session, "https://google.com", 3)
            ),
        ]
        done, pending = await asyncio.wait(pending_tasks, timeout=2)
        logger.debug("Завершенные задачи: %s", len(done))
        logger.debug("Оставшиеся задачи: %s", len(pending))
        for task in done:
            result = await task
            logger.debug("Задача выполнена успешно: %s", result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
