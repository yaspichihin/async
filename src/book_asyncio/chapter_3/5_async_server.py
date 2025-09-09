#! /usr/bin/env python3
import asyncio
import logging
import signal
import socket

from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)

TASKS = []


class GracefulShutdown(SystemExit):
    pass


def shutdown():
    raise GracefulShutdown()


async def close_tasks(tasks: list[asyncio.Task]):
    """Принимает список задач и оборачивает их в await asyncio.wait_for.
    Если задача не завершилась за 1 секунду, то обрабатываем исключение
    TimeoutError.
    """
    waiters = [asyncio.wait_for(task, timeout=1) for task in tasks]
    for waiter in waiters:
        try:
            await waiter
        except asyncio.TimeoutError:
            logger.debug("Задача %s не завершилась за 1 секунду", waiter)
        except Exception as e:
            logger.error("Неожиданная ошибка при завершении задачи: %s", e)


async def echo(conn, loop):
    # Этот try/except/finally нужен для того, чтобы закрыть
    # соединение в случае ошибки т.к. иначе ошибка это
    # результат корутины и не будет обработана как ошибка
    try:
        while data := await loop.sock_recv(conn, 1024):
            logger.debug("Получены данные: %s", data)
            if b"q" in data:
                logger.debug("Сигнал завершения: %s", data)
                raise Exception("Неожиданная ошибка")
            await loop.sock_sendall(conn, data)
    except Exception as e:
        logger.error("Ошибка: %s", e)
    finally:
        conn.close()


async def connection_listener(srv_sock, loop):
    while True:
        conn, addr = await loop.sock_accept(srv_sock)
        logger.debug("Запрос на подключение: %s", addr)
        conn.setblocking(False)
        task = asyncio.create_task(echo(conn, loop))
        TASKS.append(task)


async def main(loop: asyncio.AbstractEventLoop):
    server_address = ("127.0.0.1", 8000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.setblocking(False)
    server_socket.listen()
    logger.info("Сервер слушает %s", server_address)

    for signame in ("SIGINT", "SIGTERM"):
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await connection_listener(server_socket, loop)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    try:
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))
    except GracefulShutdown:
        logger.debug("Получен сигнал завершения. Завершаем работу сервера.")
        loop.run_until_complete(close_tasks(TASKS))
    finally:
        loop.close()
