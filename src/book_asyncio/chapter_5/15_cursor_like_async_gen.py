#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)

QUERY_PRODUCTS = "SELECT * FROM product"


async def main():
    """Пример потоковой обработки записей из БД для экономии памяти"""
    try:
        conn = await asyncpg.connect(**config.db_params)
        async with conn.transaction():
            async for product in conn.cursor(QUERY_PRODUCTS):
                logger.debug(product)
    finally:
        await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
