import datetime
import unittest
from unittest.mock import Mock, call
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

    def test_start_span(self):
        mock_client = Mock()
        tracer = Tracer(mock_client)
        span = tracer.start_trace(context={'big': 'important_stuff'})
        self.assertEqual(span, tracer._trace.stack[0])
        self.assertEqual(1, len(tracer._trace.stack))
        span2 = tracer.start_span(context={'more': 'important_stuff'})
        # should still have the root span as the first item in the stack
        self.assertEqual(span, tracer._trace.stack[0])
        self.assertEqual(span2, tracer._trace.stack[-1])
        # trace id should match what the tracer has
        self.assertEqual(span.trace_id, tracer._trace.id)
        mock_client.new_event.return_value.add.assert_has_calls([
            call(data={'more': 'important_stuff'}),
            call(data={
                'trace.trace_id': span2.trace_id,
                'trace.parent_id': span2.parent_id,
                'trace.span_id': span2.id,
            }),
        ])
