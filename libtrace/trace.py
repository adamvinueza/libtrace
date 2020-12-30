from typing import Dict, List
from libtrace.span import Span
"""
ADAPTED FROM Trace CLASS AT
    https://github.com/honeycombio/beeline-python/trace.py
"""


class Trace(object):
    """Trace objects contain Spans."""
    id: str
    stack: List[Span]
    fields: Dict

    def __init__(self, trace_id: str):
        self.id = trace_id
        self.stack = []
        self.fields = {}
