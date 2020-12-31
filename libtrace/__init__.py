from __future__ import annotations
from typing import Optional
from libtrace.span import Span
from libtrace.trace import Trace
from libtrace.tracer import Tracer
from libtrace.internal import _GLOBAL_DEBUG
import libevent

__all__ = ['Span', 'Trace']

_GLOBAL_TRACER: Optional[Tracer] = None


def get_tracer(debug: bool = False) -> Tracer:
    global _GLOBAL_TRACER

    if not _GLOBAL_TRACER:
        libevent.init()
        _GLOBAL_TRACER = Tracer(libevent.state.CLIENT)
        internal.init_logger(debug)

    return _GLOBAL_TRACER


