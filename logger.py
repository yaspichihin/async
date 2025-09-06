import logging

LOGGING_LEVEL = logging.DEBUG

format_msg = "%(levelname)s - %(name)s - %(message)s"
formatter = logging.Formatter(format_msg)

handler = logging.StreamHandler()
handler.setLevel(LOGGING_LEVEL)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(LOGGING_LEVEL)
