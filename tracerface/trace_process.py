from contextlib import redirect_stdout
from importlib import machinery, util
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty
import sys


# BCC trace is supposed to be run from the terminal.
# With this hack we can use it as a reuglar class instead.
def _get_bcc_trace_tool(args):
    sys.path.append('/usr/lib/python3/dist-packages')
    loader = machinery.SourceFileLoader('bcc_trace', '/usr/share/bcc/tools/trace')
    spec = util.spec_from_loader(loader.name, loader)
    bcc_trace = util.module_from_spec(spec)
    loader.exec_module(bcc_trace)
    sys.argv = args
    return bcc_trace.Tool()


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
        tool = _get_bcc_trace_tool(self._args)
        with redirect_stdout(self._queue):
            tool.run()

    def get_output(self):
        try:
            return self._queue.get_nowait().strip(' ')
        except Empty:
            return None
