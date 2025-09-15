#! /usr/bin/env python3
import logging
from concurrent.futures import ProcessPoolExecutor

from book_asyncio.utils import configure_logging, sync_timed

logger = logging.getLogger(__name__)


@sync_timed()
def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter += 1
    return counter


@sync_timed()
def main():
    with ProcessPoolExecutor() as pool:
        numbers = list(range(10))
        results = pool.map(count, numbers)
        for result in results:
            logger.debug(result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    main()
