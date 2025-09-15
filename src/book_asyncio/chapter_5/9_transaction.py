#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


async def main():
    conn = await asyncpg.connect(**config.db_params)
    try:
        async with conn.transaction():
            await conn.execute("INSERT INTO brand VALUES (DEFAULT, 'brand_1')")
            await conn.execute("INSERT INTO brand VALUES (DEFAULT, 'brand_2')")

        brand_query = """
        SELECT brand_name FROM brand
        WHERE brand_name LIKE 'brand_%'
        """
        brands = await conn.fetch(brand_query)
        logger.debug(brands)
    finally:
        await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
