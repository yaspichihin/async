#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


async def main():
    insert_brand_3 = "INSERT INTO brand VALUES (DEFAULT, 'brand_3')"
    brand_query = "SELECT * FROM brand WHERE brand_name LIKE 'brand_3'"

    conn = await asyncpg.connect(**config.db_params)
    transaction = conn.transaction()

    # Начало транзакции
    await transaction.start()
    try:
        await conn.execute(insert_brand_3)
    except Exception as e:
        logger.error(e)
        await transaction.rollback()
    else:
        await transaction.commit()
    finally:
        brands = await conn.fetch(brand_query)
        logger.debug(brands)
        await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
