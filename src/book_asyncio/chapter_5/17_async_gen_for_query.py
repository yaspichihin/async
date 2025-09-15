#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)

QUERY_PRODUCTS = "SELECT * FROM product"


async def take(generator, to_take):
    item_count = 0
    async for item in generator:
        if item_count >= to_take:
            return
        item_count += 1
        yield item


async def main():
    """
    Пример ограничения количества записей, получаемых из БД
    """
    try:
        conn = await asyncpg.connect(**config.db_params)
        async with conn.transaction():
            product_gen = conn.cursor(QUERY_PRODUCTS)
            async for product in take(product_gen, 5):
                logger.debug("Got product: %s", product)
    except Exception as e:
        logger.error(e)
    finally:
        await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
