#! /usr/bin/env python3
import asyncio
import logging

import aiohttp
from book_asyncio.utils import async_timed, configure_logging, fetch_status

logger = logging.getLogger(__name__)


@async_timed()
async def main() -> None:
    async with aiohttp.ClientSession() as session:
        urls = ("https://ya.ru", "https://mail.ru", "https://google.com")
        fetchers = [
            asyncio.create_task(fetch_status(session, url)) for url in urls
        ]
        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_COMPLETED
        )
        logger.debug("Завершенные задачи: %s", len(done))
        logger.debug("Оставшиеся задачи: %s", len(pending))
        for done_task in done:
            if done_task.exception() is None:
                logger.debug(
                    "Задача выполнена успешно: %s", done_task.result()
                )


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
