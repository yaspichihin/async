#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)

QUERY_PRODUCTS = "SELECT * FROM product"


async def main():
    try:
        conn = await asyncpg.connect(**config.db_params)
        tran = conn.transaction()
        await tran.start()
        curs = await conn.cursor(QUERY_PRODUCTS)
        await curs.forward(50)
        products = await curs.fetch(5)
        for product in products:
            logger.debug("Got product: %s", product)

    except Exception as e:
        logger.error(e)
        await tran.rollback()

    else:
        await tran.commit()
        logger.debug("Committed")

    finally:
        await conn.close()
        logger.debug("Closed")


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
