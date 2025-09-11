#! /usr/bin/env python3
import asyncio
import logging

import asyncpg
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging
from faker import Faker

logger = logging.getLogger(__name__)

fake = Faker("en_US")


def generate_brands(count: int) -> list[str]:
    return [(fake.company(),) for _ in range(count)]


async def insert_brands(conn: asyncpg.Connection, brands: list[str]):
    insert_brands = "INSERT INTO brand VALUES (DEFAULT, $1)"
    await conn.executemany(insert_brands, brands)


async def main():
    conn = await asyncpg.connect(**config.db_params)
    await insert_brands(conn, generate_brands(100))
    await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
