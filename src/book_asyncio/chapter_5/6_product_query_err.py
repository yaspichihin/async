#! /usr/bin/env python3
import asyncio

import asyncpg
from book_asyncio.chapter_5 import config

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


async def main():
    """
    Пример ошибки выполнения двух запросов одновременно из-за
    соответствия одного сокета к одному SQL соединению.
    """

    conn = await asyncpg.connect(**config.db_params)
    queries = (conn.execute(PRODUCT_QUERY), conn.execute(PRODUCT_QUERY))
    results = await asyncio.gather(*queries)
    print(results)
    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
