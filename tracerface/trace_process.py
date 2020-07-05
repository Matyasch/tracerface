from contextlib import redirect_stdout
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty
import sys

from tracerface.bcc_trace import Tool


# Special Queue class with a write and flush method
# which can be used to write text streams into
class WritableQueue(Queue):
    def write(self, s):
        self.put(s)

    def flush(self):
        pass


# Speacial Process class which runs the tracing
# and makes it possible to retrieve its output.
class TraceProcess(multiprocessing.Process):
    def __init__(self, args):
        super().__init__()
        self._queue = WritableQueue(ctx=multiprocessing.get_context())
        self._args = args

    def run(self):
        with redirect_stdout(self._queue):
            sys.argv = self._args
            Tool().run()

    def get_output(self):
        try:
            return self._queue.get_nowait().strip(' ')
        except Empty:
            return None
