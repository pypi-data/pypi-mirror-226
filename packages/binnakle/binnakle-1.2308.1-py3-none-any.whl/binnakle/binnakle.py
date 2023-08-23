#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
from .utils import (
    get_timestamp_ms,
    remove_empty_keys,
)
import inspect
import traceback
from os import environ


class BinnakleHandler(logging.Handler):

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = instance

    def emit(self, record):
        getattr(self._instance, record.levelname.lower())(record.getMessage())


class Binnakle:
    _instance = None

    def __new__(
        cls,
        *args,
        **kwargs,
    ):
        if not cls._instance:
            cls._instance = super(Binnakle, cls).__new__(cls)

            root_logger = logging.getLogger()

            loggers = (
                list(logging.Logger.manager.loggerDict.values())
                + [root_logger]
            )

            # Remove all handlers from all loggers and add the BinnakleHandler
            for logger in loggers:
                if hasattr(logger, 'handlers'):
                    while logger.handlers:
                        logger.removeHandler(logger.handlers[0])
                    logger.addHandler(BinnakleHandler(cls._instance))

        return cls._instance

    def __init__(
        self,
        pretty: bool = None,
        env: str = None,
        prefix: str = None,
        server_url: str = None,
        name: str = None,
        level: str = None,
    ):
        self.reload(
            pretty=pretty,
            env=env,
            prefix=prefix,
            server_url=server_url,
            name=name,
            level=level,
        )

    def reload(
        self,
        pretty: bool = None,
        env: str = None,
        prefix: str = None,
        server_url: str = None,
        name: str = None,
        level: str = None,
    ):
        if pretty is None:
            self._pretty = environ.get(
                'BINNAKLE_PRETTY',
                'false',
            ).lower() == 'true'
        else:
            self._pretty = pretty

        if env is None:
            self._env = environ.get(
                'BINNAKLE_ENV',
                'local',
            ).lower()
        else:
            self._env = env

        self._server_url = server_url
        self._prefix = prefix

        if name is None:
            self._name = environ.get(
                'BINNAKLE_NAME',
                'binnakle',
            )
        else:
            self._name = name

        self._logger = logging.getLogger(self._name)
        while self._logger.handlers:
            self._logger.removeHandler(self._logger.handlers[0])

        if level is None:
            self._level = 'INFO'
        else:
            self._level = level.upper()
        self._logger.setLevel(getattr(logging, self._level))

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self._logger.addHandler(handler)
        self._logger.propagate = False

    def set_level(
        self,
        level: str = None,
    ):
        if level is None:
            raise ValueError('level is required')
        self._logger.setLevel(getattr(logging, level.upper()))

    def wrapped(method):

        def _wrapped(
            self,
            message=None,
            error: Exception = None,
            stack_depth=None,
            **kwargs,
        ):
            if isinstance(message, bytes):
                message = message.decode('utf-8')

            if message is not None and self._prefix is not None:
                message = self._prefix + message

            if stack_depth is None:
                stack_depth = 1
            inspection = inspect.stack()[stack_depth]

            level = method.__name__.upper()
            if method.__name__ == 'exception':
                level = 'ERROR'
                error_message = traceback.format_exc()
            else:
                error_message = self._get_error_message(error)

            payload = {
                'level': level,
                'env': self._env,
                'timestamp': get_timestamp_ms(),
                'filepath': inspection.filename,
                'function': inspection.function,
                'line': inspection.lineno,
                'error': error_message,
            } | kwargs | {
                'message': message
            }
            message_dict = remove_empty_keys(payload)

            modified_message = json.dumps(
                message_dict,
                indent=4 if self._pretty else None,
                separators=None if self._pretty else (',', ':'),
                ensure_ascii=False,
            )
            return method(self, modified_message)

        return _wrapped

    @staticmethod
    def _get_error_message(error):
        if error is None:
            return

        try:
            # Python 3.10+
            error_message_lines = traceback.format_exception(error)
        except Exception:
            error_message_lines = traceback.format_exception(
                etype=type(error), value=error, tb=error.__traceback__
            )

        error_message = ''.join(error_message_lines)
        return error_message

    @wrapped
    def debug(self, message):
        self._logger.debug(message)

    @wrapped
    def info(self, message):
        self._logger.info(message)

    @wrapped
    def warning(self, message):
        self._logger.warning(message)

    warn = warning

    @wrapped
    def error(self, message):
        self._logger.error(message)

    @wrapped
    def critical(self, message):
        self._logger.critical(message)

    fatal = critical

    @wrapped
    def exception(self, message):
        self._logger.error(message)
