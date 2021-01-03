from typing import Callable
from .span import Span
from .trace import Trace
from .trace_container import TraceContainer
from .tracer import Tracer


def get_trace_container() -> TraceContainer: ...
def init(debug: bool = False) -> None: ...
def traced(name: str, trace_id: str = None, parent_id: str = None) -> Callable: ...
