from typing import Dict, Optional
from libtrace.span import Span
from libtrace.trace import Trace
from libevent import Client


class Tracer(object):
    _client: Client
    _trace: Optional[Trace]
    def __init__(self, client: Client): ...
    def finish_span(self, span) -> None: ...
    def finish_trace(self, span: Span) -> None: ...
    def start_span(self,
                   context: Optional[Dict] = None,
                   parent_id: Optional[str] = None) -> Optional[Span]: ...
    def start_trace(self,
                    context: Optional[Dict] = None,
                    parent_id: Optional[str] = None) -> Span: ...
