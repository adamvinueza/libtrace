import unittest
from libevent.event import Event
from libtrace.span import Span


class TestSpan(unittest.TestCase):
    """
    Spans have these properties:

        span.id
        span.parent_id
        span.trace_id

    Spans have these methods:

        span.add_context_field(key: str, value: Any)
        span.add_context(data: Dict)
        span.remove_context_field(key: str)
        span.fields() -> Dict

    """
    def test_span_context(self):
        ev = Event()
        span = Span("", "", "", ev)
        span.add_context_field("some", "value")
        span.add_context({"another": "value"})
        self.assertDictEqual({
            "some": "value",
            "another": "value"
        }, ev.fields())
        span.remove_context_field("another")
        self.assertDictEqual({
            "some": "value",
        }, ev.fields())
        self.assertDictEqual({
            "some": "value",
        }, span.fields())
