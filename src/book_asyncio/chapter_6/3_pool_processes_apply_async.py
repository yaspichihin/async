#! /usr/bin/env python3
import logging
import multiprocessing
import time

from book_asyncio.utils import configure_logging, sync_timed

logger = logging.getLogger(__name__)


@sync_timed()
def say_hello(name: str) -> str:
    time.sleep(10)
    return f"Hello, {name}!"


@sync_timed()
def main():
    names = ("John", "Jane", "Jim", "Jill")
    with multiprocessing.Pool() as pool:
        results = [pool.apply_async(say_hello, args=(name,)) for name in names]
        for result in results:
            result = result.get()
            logger.debug(result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    main()
