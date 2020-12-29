from io import StringIO
import logging
import unittest
import libevent
from libevent.log_handler import LogHandler
from libevent.trace import trace


@trace
def third():
    return 'third'


@trace
def second():
    return f'second, {third()}'


@trace
def first():
    return f'first, {second()}'


class TestTrace(unittest.TestCase):
    def setUp(self):
        self.stream = StringIO()
        # redirect stderr to StringIO
        lh = LogHandler.with_handler(
            name="test",
            handler=logging.StreamHandler(self.stream)
        )
        libevent.init(handlers=[lh])

    def tearDown(self):
        tr = libevent.get_tracer()
        tr.finish_trace(tr.get_active_span())

    @trace
    def test_trace(self):
        _ = first()
        self.stream.seek(0)
        lines = sum(1 for _ in self.stream)
        self.stream.seek(0)
        self.assertEqual(3, lines)
