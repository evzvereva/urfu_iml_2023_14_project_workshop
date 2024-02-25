import logging
import os
from hashlib import md5
from logging.handlers import TimedRotatingFileHandler

import yaml


def check_token(token: str) -> bool:
    """
    Функция проверяет наличие хэш-суммы токена в списке разрешенных.

    Параметры:
        token (bytes): токен

    Возвращаемое значение:
        None.
    """
    token_md5 = md5(token.encode('utf-8')).hexdigest()

    with open('secrets.txt', 'r') as file:
        hash = file.readline().strip()
        if hash == token_md5:
            return True

    return False


def add_hash(token: bytes) -> None:
    """
    Функция добавляет хэш-сумму токена в списко разрешенных.

    Параметры:
        token (bytes): токен

    Возвращаемое значение:
        None.
    """
    with open('secrets.txt', 'a') as file:
        file.write(md5(token.encode('utf-8')).hexdigest())
        file.write('\n')


def load_settings():
    with open('settings.yaml', 'r') as file:
        settings = yaml.load(file, Loader=yaml.loader.BaseLoader)
        return settings


def getLogger(name: str) -> logging.Logger:
    """
    Возвращает объект логера с переданным именем.

    Параметры:
        name (str): имя логера

    Возвращаемое значение:
        logging.Logger: объект логера.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_handler = TimedRotatingFileHandler(
        f"logs/{name}.log", encoding='utf-8', when='D'
    )
    log_formatter = logging.Formatter(
        u"%(name)s %(asctime)s %(levelname)s %(message)s"
    )
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    return logger
