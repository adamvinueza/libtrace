# libtrace

A library for tracing events.

`libtrace` is a very, very streamlined version of Honeycomb's [`beeline-python` Python
SDK](https://github.com/honeycombio/beeline-python). I wrote it mostly as an
exercise to teach myself how to build an instrumentation library, but it may
come in handy for applications as well.

To accord with the `beeline-python` license, the library source files have been
prominently documented as having been adapted from Honeycomb source files.

## Usage

Tracing is the monitoring or profiling of an application's execution. When we
trace an application's execution, we insert code logging relevant info, such
as what function is being executed, what its parameters are, when it began or
finished, whether errors occurred, etc.

`libtrace` supports basic tracing via a global `Tracer` object. To trace an
application, put a call to `libevent.get_tracer` at the start of any
instrumentation. If you begin instrumentation at the entry point of your
application, tracing will continue throughout all instrumented calls until the
application exits or the trace is explicitly finished.

Here is a sample of tracing inside an AWS Lambda function:

```python

import boto3
import libtrace
import inspect

lmb = boto3.client('lambda')

def handler(event, context):
    t = libtrace.get_tracer(auto=False)
    span = t.get_active_span()
    span.add_field('operation', inspect.stack()[1][3])
    if type(event) is dict:
        span.event.add(event)
    else:
        span.event.add_field('event', str(event))
    with span.event.timer():
        resp = lmb.get_account_settings()
    span.event.add_field('response', resp)
    t.finish_trace(span=span)
    return resp
```

## Automatic Tracing

If you want minimal instrumentation in your code, you can use decorators for
tracing automatically. Using the `@trace` decorator, the function name and
parameters will be recorded, along with the function's entry and exit times
as well as the duration, and error information if an error occurred.
```python
import boto3
from libtrace.trace import trace

lmb = boto3.client('lambda')

@trace
def handler(event, context):
    resp = lmb.get_account_settings()
    return resp
```
