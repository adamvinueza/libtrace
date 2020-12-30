from __future__ import annotations
from libtrace.span import Span
from libtrace.trace import Trace

__all__ = ['Span', 'Trace']

import libtrace.constants as constants
import random


def generate_span_id() -> str:
    format_str = "{{:0{:d}x}}".format(constants.SPAN_ID_BYTES * 2)
    sys_rand = random.SystemRandom()
    return format_str.format(
        sys_rand.getrandbits(constants.SPAN_ID_BYTES * 8))


def generate_trace_id() -> str:
    format_str = "{{:0{:d}x}}".format(constants.TRACE_ID_BYTES * 2)
    sys_rand = random.SystemRandom()
    return format_str.format(
        sys_rand.getrandbits(constants.TRACE_ID_BYTES * 8))
