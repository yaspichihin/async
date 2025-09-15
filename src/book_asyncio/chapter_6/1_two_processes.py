#! /usr/bin/env python3
import logging
from multiprocessing import Process

from book_asyncio.utils import configure_logging, sync_timed

logger = logging.getLogger(__name__)


@sync_timed()
def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter += 1


@sync_timed()
def main():
    processes = [
        Process(target=count, args=(100_000_000,)),
        Process(target=count, args=(200_000_000,)),
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    main()
