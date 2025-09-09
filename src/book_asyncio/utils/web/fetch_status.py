import asyncio
import logging

from aiohttp import ClientSession


async def fetch_status(
    session: ClientSession, url: str, delay: int = 0
) -> int:
    logger = logging.getLogger(__name__)
    if delay:
        logger.debug("Засыпаю на %s секунд", delay)
        await asyncio.sleep(delay)
    async with session.get(url) as result:
        status = result.status
        logger.debug("Url: %s, Status: %s", url, status)
        return status
