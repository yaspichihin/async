import socket

from logger import logger

server_socket = socket.socket(
    # Тип адреса (Имя хоста, номер порта)
    family=socket.AF_INET,
    # Протокол TCP
    type=socket.SOCK_STREAM,
)

# Настройка для переиспользования серверного порта.
# Позволяет не получать ошибку "Адрес уже используется
# при перезапуске приложения.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Установка адреса для серверного порта
address = ("127.0.0.1", 8000)
server_socket.bind(address)
# Запустить ожидание подключения клиентов
server_socket.listen()

client_conn = None
try:
    # При подключении клиента, завести отдельный клиентский порт.
    client_conn, client_addr = server_socket.accept()
    logger.debug("Получен запрос на подключение от %s", client_addr)

    buffer = b""
    while buffer[-2:] != b"\r\n":
        data = client_conn.recv(2)
        if data:
            logger.debug("Получена часть данных: %s", data)
            buffer += data
        else:
            break
    logger.debug("Получены данные: %s", buffer)
    # Отправить полученные данные клиенту обратно
    client_conn.sendall(buffer)
finally:
    if client_conn:
        client_conn.close()
    server_socket.close()
