import datetime
from libevent.event import Event
from typing import Dict
"""
ADAPTED FROM Span CLASS AT
    https://github.com/honeycombio/beeline-python/trace.py
"""


class Span(object):
    """Represents an active span. Create via Tracer.start_span."""
    def __init__(self,
                 trace_id: str,
                 parent_id: str,
                 id: str,
                 ev: Event,
                 is_root: bool = False):
        self.event = ev
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.id = id
        self._is_root = is_root
        """
        In beeline, start_time is a property of the event. But it's used only
        for calculating an event field, so I think it belongs in the Span.
        """
        self.start_time = datetime.datetime.now()

    def add_context(self, data: Dict):
        self.event.add(data)

    def add_context_field(self, key: str, value: str):
        self.event.add_field(key, value)

    def fields(self):
        return self.event.fields()

    @property
    def is_root(self):
        return self._is_root

    def remove_context_field(self, key):
        del(self.event[key])
