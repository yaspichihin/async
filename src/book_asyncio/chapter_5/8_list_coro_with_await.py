#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import async_timed, configure_logging

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


@async_timed()
async def query_products_sync(pool, cnt):
    """Из-за await в цикле, все запросы выполняются последовательно"""
    queries = [await query_product(pool) for _ in range(cnt)]
    return queries


@async_timed()
async def query_products_async(pool, cnt):
    """Запросы выполняются конкурентно из-за списка сопрограмм и gather"""
    queries = [query_product(pool) for _ in range(cnt)]
    return await asyncio.gather(*queries)


async def main():
    params = {
        "min_size": 50,
        "max_size": 50,
        **config.db_params,
    }
    async with asyncpg.create_pool(**params) as pool:
        await query_products_sync(pool, 10_000)  # ~ 4.7 seconds
        await query_products_async(pool, 10_000)  # ~ 0.9 seconds


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
