#! /usr/bin/env python3
import asyncio
import logging

from book_asyncio.utils import async_timed, configure_logging, delay

logger = logging.getLogger(__name__)


@async_timed()
async def main() -> None:
    # async with aiohttp.ClientSession() as session:
    #     urls = ["https://ya.ru" for _ in range(1_000)]
    #     requests = [fetch_status(session, url) for url in urls]
    #     await asyncio.gather(*requests)
    delay_times = (3 for _ in range(1_000))
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
