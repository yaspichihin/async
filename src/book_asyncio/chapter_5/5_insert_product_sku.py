#! /usr/bin/env python3
import asyncio
import logging
from random import randint

import asyncpg
import faker_commerce
from book_asyncio.chapter_5 import config
from book_asyncio.utils import configure_logging
from faker import Faker

logger = logging.getLogger(__name__)

fake = Faker("en_US")
fake.add_provider(faker_commerce.Provider)


def generate_products(cnt: int, brand_ids: list[int]) -> list[tuple[str, int]]:
    min_brand_id, max_brand_id = brand_ids
    products = []
    for _ in range(cnt):
        product_name = fake.ecommerce_name()
        brand_id = randint(min_brand_id, max_brand_id)
        products.append((product_name, brand_id))
    return products


def generate_skus(cnt: int, product_ids: list[int]) -> list[tuple[str, int]]:
    min_product_id, max_product_id = product_ids
    skus = []
    for _ in range(cnt):
        product_id = randint(min_product_id, max_product_id)
        size_id = randint(1, 3)
        color_id = randint(1, 2)
        skus.append((product_id, size_id, color_id))
    return skus


async def insert_products(
    conn: asyncpg.Connection, products: list[tuple[str, int]]
):
    insert_products = "INSERT INTO product VALUES (DEFAULT, $1, $2)"
    await conn.executemany(insert_products, products)


async def insert_skus(conn: asyncpg.Connection, skus: list[tuple[str, int]]):
    insert_skus = "INSERT INTO sku VALUES (DEFAULT, $1, $2, $3)"
    await conn.executemany(insert_skus, skus)


async def main():
    conn = await asyncpg.connect(**config.db_params)
    await insert_products(conn, generate_products(900, [1, 100]))
    await insert_skus(conn, generate_skus(100_000, [100, 999]))
    await conn.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
