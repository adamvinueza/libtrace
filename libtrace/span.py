from libevent.event import Event
from typing import Dict
"""
ADAPTED FROM Span CLASS AT https://github.com/honeycombio/beeline-python/trace.py
"""


class Span(object):
    """Represents an active span. Create via Tracer.start_span."""
    def __init__(self,
                 trace_id: str,
                 parent_id: str,
                 id: str,
                 ev: Event):
        self.event = ev
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.id = id

    def add_context(self, data: Dict):
        self.event.add(data)

    def add_context_field(self, key: str, value: str):
        self.event.add_field(key, value)

    def fields(self):
        return self.event.fields()

    def remove_context_field(self, key):
        del(self.event[key])
