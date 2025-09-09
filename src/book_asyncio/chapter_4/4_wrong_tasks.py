import asyncio
import logging

from book_asyncio.utils import async_timed, configure_logging, delay

logger = logging.getLogger(__name__)


@async_timed()
async def main() -> None:
    delay_times = (3, 3, 3)
    for seconds in delay_times:
        await asyncio.create_task(delay(seconds))


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
