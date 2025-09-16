#! /usr/bin/env python3
import json

from book_asyncio.utils import configure_logging, sync_timed

FILE_READ = "src/book_asyncio/chapter_6/googlebooks-eng-all-1gram-a"
FILE_WRITE = "src/book_asyncio/chapter_6/sync_1_gram.json"


# Функция get_parts завершилась за 20.6635 с
def get_parts(filepath: str) -> dict:
    with open(filepath, encoding="utf-8") as file:
        parts = file.readlines()
    return parts


# Просто Killed не хватает памяти в 15 Гб при этом построчная
# обработка for line in file при чтении работает, но не заложена
# в обучающем примере.
def count_words(parts: list[str]) -> dict:
    freq = {}
    for part in parts:
        word, _, count, _ = part.split("\t")
        freq[word] = freq.get(word, 0) + int(count)
    return freq


def write_to_file(filepath: str, data: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)


def parts_generator(filepath: str):
    with open(filepath, encoding="utf-8") as file:
        yield from file


# Функция main завершилась за 42.7643 с
@sync_timed()
def main():
    # parts = get_parts(FILE_READ)
    # cnt = count_words(parts)
    # write_to_file(FILE_WRITE, cnt)

    # Перепишу на поточную обработку
    parts = parts_generator(FILE_READ)
    cnt = count_words(parts)
    write_to_file(FILE_WRITE, cnt)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    main()
