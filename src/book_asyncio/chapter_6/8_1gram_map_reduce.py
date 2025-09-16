#! /usr/bin/env python3
import asyncio
import concurrent
from functools import partial, reduce

from book_asyncio.utils import configure_logging, sync_timed

FILE_READ = "src/book_asyncio/chapter_6/googlebooks-eng-all-1gram-a"
FILE_WRITE = "src/book_asyncio/chapter_6/sync_1_gram_map_reduce.json"


@sync_timed()
def get_parts(filepath: str) -> dict:
    with open(filepath, encoding="utf-8") as file:
        parts = file.readlines()
    return parts


@sync_timed()
def partition(parts: list[str], chunk_size: int):
    for i in range(0, len(parts), chunk_size):
        yield parts[i : i + chunk_size]


@sync_timed()
def map_freq(chunk: list[str]) -> dict:
    freq = {}
    for line in chunk:
        word, _, count, _ = line.split("\t")
        freq[word] = freq.get(word, 0) + int(count)
    return freq


@sync_timed()
def merge_dicts(d1: dict, d2: dict) -> dict:
    words = set(d1.keys()) | set(d2.keys())
    merged = {w: d1.get(w, 0) + d2.get(w, 0) for w in words}
    return merged


@sync_timed()
async def reduce_freq(loop, pool, cnt, chunk) -> dict:
    chunks = list(partition(cnt, chunk))
    reducers = []
    while len(chunks[0]) > 1:
        for chunk in chunks:
            reducer = partial(reduce, merge_dicts, chunk)
            reducers.append(loop.run_in_executor(pool, reducer))
        reducer_chunks = await asyncio.gather(*reducers)
        chunks = list(partition(reducer_chunks, chunk))
        reducers.clear()
    return chunks[0][0]


@sync_timed()
async def main(partition_size: int = 60_000):
    parts = get_parts(FILE_READ)

    loop = asyncio.get_event_loop()

    tasks = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for chunk in partition(parts, partition_size):
            part = partial(map_freq, chunk)
            tasks.append(loop.run_in_executor(executor, part))

        all_freq = await asyncio.gather(*tasks)
        total_freq = await reduce_freq(
            loop, executor, all_freq, partition_size=500
        )
        print("Aardvark: %s" % total_freq["Aardvark"])


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
