from typing import Dict, List
from libtrace.span import Span


class Trace(object):
    """Trace objects contain Spans."""
    id: str
    stack: List[Span]
    fields: Dict

    def __init__(self, trace_id: str):
        self.id = trace_id
        self.stack = []
        self.fields = {}
