from __future__ import annotations
from typing import Optional
from libtrace.span import Span
from libtrace.trace import Trace
from libtrace.tracer import Tracer
import libevent
import logging
import sys

__all__ = ['Span', 'Trace']

_GLOBAL_TRACER: Optional[Tracer] = None
_GLOBAL_LOGGER: logging.Logger
_GLOBAL_DEBUG: bool = False


def get_tracer(debug: bool = False) -> Tracer:
    global _GLOBAL_TRACER
    global _GLOBAL_LOGGER
    global _GLOBAL_DEBUG

    if not _GLOBAL_TRACER:
        libevent.init()
        _GLOBAL_TRACER = Tracer(libevent.state.CLIENT)
        _GLOBAL_LOGGER = logging.Logger('libtrace')
        _GLOBAL_LOGGER.setLevel(logging.DEBUG)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        _GLOBAL_LOGGER.addHandler(sh)
        _GLOBAL_DEBUG = debug

    return _GLOBAL_TRACER


def log(msg: str, *args, **kwargs) -> None:
    if _GLOBAL_DEBUG:
        _GLOBAL_LOGGER.debug(msg, *args, **kwargs)
