from typing import Optional
from .tracer import Tracer
import logging


_GLOBAL_TRACER: Optional[Tracer] = None
_GLOBAL_LOGGER: logging.Logger
_GLOBAL_DEBUG: bool = False


def get_tracer() -> Tracer: ...
def log(msg: str, *args, **kwargs) -> None: ...
