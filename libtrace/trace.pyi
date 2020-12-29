from typing import Dict, List
from libtrace.span import Span


class Trace(object):
    id: str
    stack: List[Span]
    fields: Dict
    def __init__(self, trace_id: str) -> None: ...
