#! /usr/bin/env python3
import logging

from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


def positive_digits(until: int = 9):
    if not isinstance(until, int) or not 0 < until < 10:
        err_msg = f"until must be an integer between 0 and 10: {until}"
        logger.error(err_msg)
        raise ValueError(err_msg)
    for i in range(1, until + 1):
        logger.debug(f"yielding {i}")
        yield i


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    digits = positive_digits(9)
    for _ in digits:
        continue
