import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s | %(name)s:%(process)d:%(lineno)d | %(levelname)s | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'verbose': {
            'formatter': 'simple',
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        __name__: {
            'level': 'ERROR',
            'handlers': [
                'verbose',
            ],
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


class LoggerMeta(type):
    _logger: logging.Logger = logging.getLogger(__name__)

    def __getattr__(cls, name):
        return getattr(cls._logger, name)


# noinspection PyPep8Naming
class logger(metaclass=LoggerMeta):
    @classmethod
    def setLevel(cls, level: int) -> None:
        if level == 1:
            cls._logger.setLevel(logging.WARNING)
            cls._logger.handlers[0].setLevel(logging.WARNING)
        elif level == 2:
            cls._logger.setLevel(logging.INFO)
            cls._logger.handlers[0].setLevel(logging.INFO)
        elif level == 3:
            cls._logger.setLevel(logging.DEBUG)
            cls._logger.handlers[0].setLevel(logging.DEBUG)
        elif level == 4:
            cls._logger.setLevel(5)
            cls._logger.handlers[0].setLevel(5)

    @classmethod
    def trace(cls, *args, **kwargs):
        cls._logger.log(5, *args, **kwargs)
