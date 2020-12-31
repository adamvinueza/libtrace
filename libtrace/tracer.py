import datetime
from typing import Dict, Optional
from libtrace.generate import generate_trace_id, generate_span_id
from libtrace.span import Span
from libtrace.trace import Trace
from libevent import Client
from libtrace import log

"""
ADAPTED FROM Tracer CLASS AT
    https://github.com/honeycombio/beeline-python/trace.py
"""


class Tracer(object):
    _client: Client
    _trace: Optional[Trace]

    def __init__(self, client: Client):
        self._client = client
        self._trace = None

    def finish_span(self, span) -> None:
        # no span, nothing to do
        if span is None:
            return
        # no trace, nothing to do
        if not self._trace:
            log('warning: span finished without an active trace')
            return
        if span.event:
            for k, v in self._trace.fields.items():
                if k not in span.event.fields():
                    span.event.add_field(k, v)

            duration = datetime.datetime.now() - span.start_time
            duration_ms = duration.total_seconds() * 1000.0
            span.event.add_field('duration_ms', duration_ms)

            """
            The honeycomb method is _run_hooks_and_send, and it's
            run against the Span.
            """
            span.event.send()
        else:  # something has gone horribly wrong
            log('warning: span has no event, was it initialized correctly?')

        # TBD: a bunch of checks to manage corrupt state

        self._trace.stack.pop()

    def finish_trace(self, span: Span) -> None:
        self.finish_span(span)
        self._trace = None

    def start_trace(self,
                    context: Optional[str] = None,
                    parent_span_id: Optional[str] = None) -> Span:
        if not self._trace:
            self._trace = Trace(trace_id=generate_trace_id())
        return self.start_span(context=context, parent_id=parent_span_id)

    def start_span(self,
                   context: Optional[Dict] = None,
                   parent_id: Optional[str] = None) -> Optional[Span]:
        if not self._trace:
            return None
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
                    parent_id=parent_span_id,
                    id=span_id,
                    ev=evt)
        self._trace.stack.append(span)
        return span
