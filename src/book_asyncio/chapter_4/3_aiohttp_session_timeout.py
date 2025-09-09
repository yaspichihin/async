import asyncio
import logging

import aiohttp
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


async def fetch_status(session: aiohttp.ClientSession, url: str) -> int:
    ten_mills = aiohttp.ClientTimeout(total=0.1)
    async with session.get(url, timeout=ten_mills) as response:
        return response.status


async def main():
    session_timeout = aiohttp.ClientTimeout(total=1, connect=0.2)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = "https://ya.ru"
        status = await fetch_status(session, url)
        logger.debug("Url: %s, Status: %s", url, status)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
