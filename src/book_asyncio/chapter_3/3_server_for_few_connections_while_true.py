#! /usr/bin/env python3
import logging
import socket

from book_asyncio.utils import configure_logging

logger = logging.getLogger(__name__)


def main():
    server_address = ("127.0.0.1", 8000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen()
    server_socket.setblocking(False)
    logger.info("Сервер слушает %s", server_address)

    client_connections = []
    try:
        while True:
            try:
                # При подключении клиента, завести отдельный клиентский порт.
                client_conn, client_addr = server_socket.accept()
                client_conn.setblocking(False)
                client_connections.append(client_conn)
                logger.debug(
                    "Получен запрос на подключение от %s", client_addr
                )
            except BlockingIOError:
                pass

            for conn in client_connections:
                try:
                    buffer = b""
                    while buffer[-2:] != b"\r\n":
                        data = conn.recv(2)
                        if data:
                            logger.debug("Получена часть данных: %s", data)
                            buffer += data
                        else:
                            break
                    logger.debug("Получены данные: %s", buffer)
                    conn.sendall(buffer)
                except BlockingIOError:
                    pass
    finally:
        if client_connections:
            for conn in client_connections:
                conn.close()
        server_socket.close()


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    main()
