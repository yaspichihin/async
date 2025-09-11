#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


async def main():
    conn = await asyncpg.connect(**config.db_params)
    version = conn.get_server_version()
    logger.debug("Connected to PostgreSQL %s", version)
    await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
