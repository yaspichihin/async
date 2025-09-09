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
        pending_tasks = [
            asyncio.create_task(fetch_status(session, url)) for url in urls
        ]

        done_tasks = []
        logger.debug("Завершенные задачи: %s", len(done_tasks))
        logger.debug("Оставшиеся задачи: %s", len(pending_tasks))
        while pending_tasks:
            done, _ = await asyncio.wait(
                pending_tasks, return_when=asyncio.FIRST_COMPLETED
            )

            for done_task in done:
                if done_task.exception() is None:
                    logger.debug(
                        "Задача выполнена успешно: %s", done_task.result()
                    )
                    done_tasks.append(done_task)
                    pending_tasks.remove(done_task)

            logger.debug("Завершенные задачи: %s", len(done_tasks))
            logger.debug("Оставшиеся задачи: %s", len(pending_tasks))


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
