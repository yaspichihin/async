#! /usr/bin/env python3
import asyncio
import logging

from book_asyncio.utils import async_timed, configure_logging, delay

logger = logging.getLogger(__name__)


async def positive_digits(until: int = 9):
    """Не выполняет сопрограммы конкурентно, а порождает их последовательно"""
    if not isinstance(until, int) or not 0 < until < 10:
        err_msg = f"until must be an integer between 0 and 10: {until}"
        logger.error(err_msg)
        raise ValueError(err_msg)
    for i in range(1, until + 1):
        await delay(i)
        logger.debug(f"yielding {i}")
        yield i


@async_timed()
async def main():
    digits = positive_digits(9)
    async for _ in digits:
        continue


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
