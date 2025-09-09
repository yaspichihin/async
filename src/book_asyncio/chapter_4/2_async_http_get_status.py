#! /usr/bin/env python3
import asyncio
import logging

import aiohttp
from book_asyncio.utils import async_timed, configure_logging, fetch_status

logger = logging.getLogger(__name__)


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://ya.ru"
        status = await fetch_status(session, url)
        logger.debug("Состояние для %s было равно %s", url, status)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
