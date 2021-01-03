from __future__ import annotations
from typing import Callable, Optional
from libtrace.span import Span
from libtrace.trace import Trace
from libtrace.trace_container import TraceContainer
from libtrace.tracer import Tracer
import libtrace.tracer as tracer

__all__ = ['Span', 'Trace', 'Tracer']

_GLOBAL_TRACE_CONTAINER: TraceContainer = None


def init(debug: bool = False):
    global _GLOBAL_TRACE_CONTAINER
    if _GLOBAL_TRACE_CONTAINER is None:
        _GLOBAL_TRACE_CONTAINER = TraceContainer(debug=debug)


def get_trace_container() -> TraceContainer:
    return _GLOBAL_TRACE_CONTAINER


def tracer_fn(name: str,
              trace_id: Optional[str] = None,
              parent_id: Optional[str] = None):
    tc = get_trace_container()
    if tc:
        return tc.tracer(name, trace_id, parent_id)


def traced(name: str, trace_id: str = None, parent_id: str = None) -> Callable:
    return tracer.traced(tracer_fn=tracer_fn,
                         name=name,
                         trace_id=trace_id,
                         parent_id=parent_id)
