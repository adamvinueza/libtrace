import unittest
from libtrace import Trace


class TestTrace(unittest.TestCase):
    def test_trace_init(self):
        trace_id = "12345"
        trace = Trace(trace_id=trace_id)
        self.assertEqual(trace_id, trace.id)
        self.assertListEqual([], trace.stack)
        self.assertDictEqual({}, trace.fields)
