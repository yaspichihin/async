import selectors
import socket
from selectors import SelectorKey

from logger import logger

server_address = ("127.0.0.1", 8000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.setblocking(False)

selector = selectors.DefaultSelector()
selector.register(server_socket, selectors.EVENT_READ)

server_socket.listen()
logger.info("Сервер %s инициализирован", str(server_address))

while True:
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)

    for event, _ in events:
        # Получить сокет для которого произошло событие
        event_socket = event.fileobj

        # Если событие связано с серверным сокетом,
        # то это попытка подключения.
        if event_socket == server_socket:
            client_conn, client_addr = server_socket.accept()
            client_conn.setblocking(False)
            logger.debug("Получен запрос на подключение от %s", client_addr)
            selector.register(client_conn, selectors.EVENT_READ)
        # Получить данные от клиента и отправить их обратно
        else:
            data = event_socket.recv(1024)
            logger.debug("От %s получены данные %s", event_socket, data)
            event_socket.send(data)
