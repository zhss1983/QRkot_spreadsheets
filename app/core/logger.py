import logging

from asynclog import AsyncLogDispatcher

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


class HTTPExceptionLogged:

    def debug(self, func):
        """Не реализовано"""
        pass

    def info(self, func):
        """Не реализовано"""
        pass

    def warning(self, func):
        """Не реализовано"""
        pass

    def error(self, func):
        def wrapper(*argv, **kwargv):
            http_exception = func(*argv, **kwargv)
            logger.error(jsonable_encoder(http_exception))
            return http_exception
        return wrapper

    def critical(self, func):
        """Не реализовано"""
        pass


def write_info_log(msg):
    """Реализация собственного метода регистрации логов уровня INFO"""
    print('INFO:', msg)


def write_warning_log(msg):
    """Реализация собственного метода регистрации логов уровня WARNING"""
    print('WARNING:', msg)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler_info = AsyncLogDispatcher(write_info_log)
handler_info.setLevel(logging.INFO)

logger.addHandler(handler_info)

handler_warning = AsyncLogDispatcher(write_warning_log)
handler_warning.setLevel(logging.WARNING)

logger.addHandler(handler_warning)

HTTPException = HTTPExceptionLogged().error(HTTPException)
