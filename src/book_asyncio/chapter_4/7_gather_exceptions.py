#! /usr/bin/env python3
import asyncio
import logging

import aiohttp
from book_asyncio import utils as utl

logger = logging.getLogger(__name__)


@utl.async_timed()
async def with_return_exceptions() -> None:
    """gather с return_exceptions=True вернет исключения в виде результата.

    Если произошло несколько исключений, то поймаем все исключения в точке
    await.
    """
    async with aiohttp.ClientSession() as session:
        urls = ["https://ya.ru", "https://ya.ruu"]
        requests = [utl.fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*requests, return_exceptions=True)
        exceptions = [res for res in results if isinstance(res, Exception)]
        successes = [res for res in results if not isinstance(res, Exception)]
        logger.debug("Успехи: %s", successes)
        logger.debug("Исключения: %s", exceptions)


@utl.async_timed()
async def without_return_exceptions() -> None:
    """В gather режим return_exceptions=False по умолчанию. Если хотя бы
    одно исключение, то gather выбросит исключение в точке await. Если
    есть обработка данного исключения, то другие задачи продолжат выполнение.

    Если произошло несколько исключений, то gather выбросит только первое
    исключение в точке await.
    """
    async with aiohttp.ClientSession() as session:
        urls = ["https://ya.ru", "httpsss://ya.ru"]
        requests = [utl.fetch_status(session, url) for url in urls]
        try:
            await asyncio.gather(*requests)
        except Exception as e:
            logger.error("Произошло исключение: %s", e)


async def main() -> None:
    await with_return_exceptions()
    await without_return_exceptions()


if __name__ == "__main__":
    utl.configure_logging(level="DEBUG")
    asyncio.run(main())
