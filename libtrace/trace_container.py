from libtrace.tracer import Tracer
import logging
import libevent


class TraceContainer(object):
    tracer: Tracer
    logger: logging.Logger
    debug: bool

    def __init__(self, debug: bool = False):
        libevent.init()
        self.debug = debug
        self.tracer = Tracer(client=libevent.state.CLIENT)  # type:ignore
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        self.logger = logging.Logger('libtrace')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)
