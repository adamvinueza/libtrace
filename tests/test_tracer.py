import datetime
import unittest
from unittest.mock import Mock, call
from libtrace.tracer import Tracer
from typing import Any
import libevent
import libtrace

"""
Based on classes in
    https://github.com/honeycombio/beeline-python/beeline/test_trace.py
"""


class TestTracer(unittest.TestCase):
    def setUp(self) -> None:
        libtrace.init()

    def test_start_trace(self):
        mock_client = Mock(spec_set=libevent.Client)
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
        mock_client = Mock(spec_set=libevent.Client)
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

    def test_start_span_without_trace(self):
        mock_client = Mock(spec_set=libevent.Client)
        tracer = Tracer(mock_client)
        span = tracer.start_span(context={'more': 'important_stuff'})
        self.assertIsNone(span)
        self.assertIsNone(tracer._trace)

    def test_finish_trace(self):
        mock_client = Mock(spec_set=libevent.Client)
        mock_client.new_event.return_value.start_time = datetime.datetime.now()
        tracer = Tracer(mock_client)

        span = tracer.start_trace(context={'big': 'important_stuff'})
        self.assertEqual(tracer._trace.stack[0], span)

        tracer.finish_trace(span)
        # ensure the event is sent
        mock_event: Any = span.event  # a typing hack: we know this is a mock
        mock_event.send.assert_called_once()
        # ensure that there is no current trace
        self.assertIsNone(tracer._trace)
