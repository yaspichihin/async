#! /usr/bin/env python3
import logging
import multiprocessing
import platform
import time

from book_asyncio.utils import configure_logging, sync_timed

logger = logging.getLogger(__name__)


@sync_timed()
def say_hello(name: str) -> str:
    time.sleep(10)
    return f"Hello, {name}!"


def log_system_info(logger: logging.Logger):
    logger.debug(
        "CPU count: %s, OS: %s, Platform: %s, Python version: %s",
        multiprocessing.cpu_count(),
        platform.system(),
        platform.platform(),
        platform.python_version(),
    )


@sync_timed()
def main():
    """
    Метод apply блокирует выполнение пока не завершится процесс.
    Если say_hello выполняется 10 секунд. Так как у нас 4 имени,
    то все выполнение займет 40 секунд.
    """
    names = ("John", "Jane", "Jim", "Jill")
    with multiprocessing.Pool() as pool:
        results = [pool.apply(say_hello, args=(name,)) for name in names]
    for result in results:
        logger.debug(result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    log_system_info(logger)
    main()
