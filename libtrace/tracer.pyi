from typing import Dict, Optional
from libtrace.span import Span
from libtrace.trace import Trace
from libevent import Client


class Tracer(object):
    _client: Client
    _trace: Optional[Trace]
    def __init__(self, client: Client): ...
    def start_span(self,
                   context: Optional[Dict],
                   parent_id: Optional[str]) -> Span: ...
    def start_trace(self,
                    context: Optional[Dict],
                    parent_id: Optional[str]) -> Span: ...
