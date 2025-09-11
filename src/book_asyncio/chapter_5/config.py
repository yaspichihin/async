import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="./src/book_asyncio/chapter_5/.env")

db_params = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
}
