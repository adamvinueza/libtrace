from typing import Callable, Dict, Optional
from libtrace.span import Span
from libtrace.trace import Trace
from libevent import Client


class Tracer(object):
    _client: Client
    _trace: Optional[Trace]
    def __init__(self, client: Client): ...
    def __call__(self, name: str, trace_id: str = None, parent_id: str = None): ...
    def get_active_trace_id(self) -> Optional[str]: ...
    def finish_span(self, span) -> None: ...
    def finish_trace(self, span: Span) -> None: ...
    def start_span(self,
                   context: Optional[Dict] = None,
                   parent_id: Optional[str] = None) -> Optional[Span]: ...
    def start_trace(self,
                    context: Optional[Dict] = None,
                    trace_id: Optional[str] = None,
                    parent_id: Optional[str] = None) -> Span: ...


def traced(tracer_fn: Callable,
           name: str,
           trace_id: Optional[str] = None,
           parent_id: str = None) -> Callable: ...
