import logging
import sys

_GLOBAL_LOGGER: logging.Logger
_GLOBAL_DEBUG: bool = False


def init_logger(debug: bool = False) -> None:
    global _GLOBAL_LOGGER
    global _GLOBAL_DEBUG

    _GLOBAL_LOGGER = logging.Logger('libtrace')
    _GLOBAL_LOGGER.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    _GLOBAL_LOGGER.addHandler(sh)
    _GLOBAL_DEBUG = debug


def log(msg: str, *args, **kwargs) -> None:
    if _GLOBAL_DEBUG:
        _GLOBAL_LOGGER.debug(msg, *args, **kwargs)
