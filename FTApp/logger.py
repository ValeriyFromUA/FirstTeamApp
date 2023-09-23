import logging

_log_format = "%(asctime)s - [%(levelname)s] - %(filename)s --> def %(funcName)s --> line: #%(lineno)d - %(message)s"


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_stream_handler())
    return logger
