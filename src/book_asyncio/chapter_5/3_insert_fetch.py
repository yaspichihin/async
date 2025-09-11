#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


async def main():
    conn = await asyncpg.connect(**config.db_params)
    statement_inserts = {
        "insert brand": """
        INSERT INTO brand VALUES (DEFAULT, 'Levis');
        INSERT INTO brand VALUES (DEFAULT, 'Seven');
        """,
    }
    statement_fetches = {
        "fetch brands": """
        SELECT  brand_id, brand_name FROM brand;
        """,
    }

    for table_name, statement in statement_inserts.items():
        logger.debug("Executing statement: %s", table_name)
        results = await conn.execute(statement)
    for table_name, statement in statement_fetches.items():
        logger.debug("Executing statement: %s", table_name)
        results: list[asyncpg.Record] = await conn.fetch(statement)
        for result in results:
            logger.debug(
                "id: %s, name: %s",
                result["brand_id"],
                result["brand_name"],
            )
    await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
