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
            insert_brand_1 = "INSERT INTO brand VALUES (10000, 'brand_3')"
            insert_brand_2 = "INSERT INTO brand VALUES (1, 'brand_1')"
            await conn.execute(insert_brand_1)
            await conn.execute(insert_brand_2)

    except Exception as e:
        logger.error(e)

    finally:
        brand_query = """
        SELECT brand_name FROM brand
        WHERE brand_name LIKE 'brand_3'
        """
        brands = await conn.fetch(brand_query)
        logger.debug(brands)
        await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
