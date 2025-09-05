import asyncio
import socket
from logger import logger


async def echo(conn, loop):
    while data := await loop.sock_recv(conn, 1024):
        if data == b"q":
            raise Exception("Неожиданная ошибка")
        await loop.sock_sendall(conn, data)


async def listen_connections(srv_sock, loop):
    while True:
        conn, addr = await loop.sock_accept(srv_sock)
        logger.debug("Запрос на подключение: %s", addr)
        conn.setblocking(False)
        asyncio.create_task(echo(conn, loop))


async def main():
    server_address = ("127.0.0.1", 8000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen()
    await listen_connections(server_socket, asyncio.get_event_loop())


if __name__ == "__main__":
    asyncio.run(main())
