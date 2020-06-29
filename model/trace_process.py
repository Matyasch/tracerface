from contextlib import redirect_stdout
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty
import sys

from model.bcc_trace import Tool


# Special Queue class with write method
# as an alias for put.
class WritableQueue(Queue):
    def write(self, s):
        self.put(s)
    def flush(self):
        pass


# Speacial Process class which runs the tracing and
# starts a thread to put its prints into the queue.
class TraceProcess(multiprocessing.Process):
    def __init__(self, args):
        super().__init__()
        self._queue = WritableQueue(ctx=multiprocessing.get_context())
        self._args = args

    def run(self):
        self._alive = True
        with redirect_stdout(self._queue):
            self._run_bcc_trace()

    def get_output(self):
        try:
            return self._queue.get_nowait().strip(' ')
        except Empty:
            return None

    # Make sure the process exits in case tracing fails
    def _run_bcc_trace(self):
        sys.argv = self._args
        Tool().run()
