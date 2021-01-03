import libtrace


def log(msg: str, *args, **kwargs) -> None:
    tc = libtrace.get_trace_container()
    if tc.debug:
        tc.logger.debug(msg, *args, **kwargs)
