#! /usr/bin/env python3
import asyncio
import logging
import socket

from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


class ConnectedSocket:
    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        logger.debug("Вход в контекстный менеджер, ожидание подключения")
        loop = asyncio.get_event_loop()
        conn, addr = await loop.sock_accept(self._server_socket)
        self._connection = conn
        logger.debug("Подключение подтверждено")
        return self._connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Выход из контекстного менеджера")
        self._connection.close()
        logger.debug("Подключение закрыто")


async def main():
    loop = asyncio.get_event_loop()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ("127.0.0.1", 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    logger.info("Сервер слушает %s", server_address)

    async with ConnectedSocket(server_socket) as conn:
        data = await loop.sock_recv(conn, 1024)
        logger.debug(data)


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    asyncio.run(main())
