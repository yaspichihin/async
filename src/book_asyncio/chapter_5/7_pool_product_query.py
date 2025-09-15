#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)

PRODUCT_QUERY = """
SELECT
	p.product_id,
	p.product_name,
	p.brand_id,
	s.sku_id,
	pc.product_color_name,
	ps.product_size_name
FROM product p
JOIN sku s USING(product_id)
JOIN product_color pc USING(product_color_id)
JOIN product_size ps USING(product_size_id)
WHERE p.brand_id = 100;
"""


async def query_product(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        return await conn.fetchrow(PRODUCT_QUERY)


async def main():
    params = {
        "min_size": 6,
        "max_size": 6,
        **config.db_params,
    }
    async with asyncpg.create_pool(**params) as pool:
        query_results = await asyncio.gather(
            query_product(pool),
            query_product(pool),
        )

    for query_result in query_results:
        logger.debug(query_result)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
