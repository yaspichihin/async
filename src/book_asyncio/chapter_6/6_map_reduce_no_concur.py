#! /usr/bin/env python3

from functools import reduce


def read_file(file_path: str) -> list[str]:
    with open(file_path) as file:
        return file.readlines()


def remove_punctuation(text: str) -> str:
    symbols = ".,!?:;()[]\"'"
    for symbol in symbols:
        text = text.replace(symbol, "")
    return text


def normalize_text(text: str) -> str:
    text = remove_punctuation(text)
    text = text.lower()
    return text


def map_word_frequency(text: str) -> dict[str, int]:
    text = normalize_text(text)
    return {word: text.count(word) for word in text.split()}


def merge_word_frequency(wf1, wf2):
    all_words = set(wf1) | set(wf2)
    return {word: wf1.get(word, 0) + wf2.get(word, 0) for word in all_words}


def main():
    parts = read_file("src/book_asyncio/chapter_6/words.txt")
    map_results = [map_word_frequency(part) for part in parts]
    total = reduce(merge_word_frequency, map_results)
    print(total)


if __name__ == "__main__":
    main()
