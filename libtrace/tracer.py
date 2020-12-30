import random
from typing import Dict, Optional
from libtrace import generate_trace_id, generate_span_id
from libtrace.span import Span
from libtrace.trace import Trace
from libevent import Client
"""
ADAPTED FROM Tracer CLASS AT https://github.com/honeycombio/beeline-python/trace.py
"""


class Tracer(object):
    _client: Client
    _trace: Optional[Trace]

    def __init__(self, client: Client):
        self._client = client
        self._trace = None

    def start_trace(self,
                    context: Optional[str] = None,
                    trace_id: Optional[str] = None,
                    parent_span_id: Optional[str] = None) -> Span:
        if not self._trace:
            self._trace = Trace(trace_id=trace_id)
        else:
            self._trace = Trace(trace_id=generate_trace_id())
        return self.start_span(context=context, parent_id=parent_span_id)

    def start_span(self,
                   context: Optional[Dict] = None,
                   parent_id: Optional[str] = None) -> Span:
        span_id = generate_span_id()
        evt = self._client.new_event(data=context)
        if parent_id:
            parent_span_id = parent_id
        else:
            parent_span_id = self._trace.stack[-1].id \
                if self._trace.stack else None
        if context:
            evt.add(data=context)
        evt.add(data={
            'trace.trace_id': self._trace.id,
            'trace.parent_id': parent_span_id,
            'trace.span_id': span_id,
        })
        span = Span(trace_id=self._trace.id,
                    parent_id=parent_id,
                    id=span_id,
                    ev=evt)
        self._trace.stack.append(span)
        return span

