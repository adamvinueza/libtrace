import datetime
import unittest
from unittest.mock import Mock, call
from libevent import Client
from libtrace.tracer import Tracer


class TestTracer(unittest.TestCase):
    def test_start_trace(self):
        mock_client = Mock()
        mock_client.new_event.return_value.start_time = datetime.datetime.now()
        tracer = Tracer(mock_client)
        span = tracer.start_trace(context={'big': 'important_stuff'})
        self.assertIsInstance(span.event.start_time, datetime.datetime)
        mock_client.new_event.return_value.add.assert_has_calls([
            call(data={'big': 'important_stuff'}),
            call(data={
                'trace.trace_id': span.trace_id,
                'trace.parent_id': span.parent_id,
                'trace.span_id': span.id,
            }),
        ])
