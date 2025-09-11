#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.chapter_5 import tables as t
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


async def main():
    conn = await asyncpg.connect(**config.db_params)
    statement_creates = {
        "brand": t.CREATE_BRAND_TABLE,
        "product": t.CREATE_PRODUCT_TABLE,
        "product_color": t.CREATE_PRODUCT_COLOR_TABLE,
        "product_size": t.CREATE_PRODUCT_SIZE_TABLE,
        "sku": t.CREATE_SKU_TABLE,
    }
    statement_inserts = {
        "product_color insert": t.PRODUCT_COLOR_INSERT,
        "product_size insert": t.PRODUCT_SIZE_INSERT,
    }
    for table_name, statement in statement_creates.items():
        logger.debug("Creating table: %s", table_name)
        await conn.execute(statement)
    for table_name, statement in statement_inserts.items():
        logger.debug("Inserting data into table: %s", table_name)
        await conn.execute(statement)
    await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
