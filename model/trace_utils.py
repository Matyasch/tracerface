import sys
from io import StringIO
from multiprocessing import Process
from threading import Thread, Lock
from contextlib import redirect_stdout

from env.bcc_trace import Tool
from model.utils import STACK_END_PATTERN


# Special StringIO class with atomic read and
# write operations. Reading clears the contents.
class AtomicStringIo(StringIO):
    def __init__(self):
        super().__init__()
        self.lock = Lock()

    def write(self, b):
        self.lock.acquire()
        super().write(b)
        self.lock.release()

    def getvalue(self):
        self.lock.acquire()
        val =  super().getvalue()
        super().truncate(0)
        super().seek(0)
        self.lock.release()
        return val


# Speacial Process class which runs the tracing and
# starts a thread to put its prints into the queue.
class TraceProcess(Process):
    def __init__(self, queue, args):
        super().__init__()
        self._queue = queue
        self._alive = False
        self._args = args
        self.error = None

    def run(self):
        self._alive = True
        string_io = AtomicStringIo()
        put_thread = Thread(target=self._put, args=(string_io,))
        put_thread.start()
        with redirect_stdout(string_io):
            self._run_bcc_trace()

    # Stacks are seperated by one empty line in bcc trace output.
    # This means that two newlines after eachother ('\n\n') signal
    # the start of a new stack. However these separations can be
    # in the middle of outputs and there can be several of them
    # hence we need this complicated method to parse the output.
    def _put(self, string_io):
        current_stack = ''
        while self._alive:
            output = string_io.getvalue()
            # We add the output to the currently processed stack
            current_stack += output
            # If we find a separation, we split the output on it (them)
            if '\n\n' in current_stack:
                stacks = current_stack.split('\n\n')
                # In case the output is like this: 'stack1\n\nstack2\n\nstack3...',
                # we process all the split parts except the last one, since that
                # stack have not ended yet (no separation at the end).
                for stack in stacks[:-1]:
                    for line in stack.strip().splitlines():
                        self._queue.put(line.strip())
                    # We singal the end of the stack to the model in a clear way
                    self._queue.put(STACK_END_PATTERN)
                # The last stack is not ended yet so we make it the current stack
                current_stack = stacks[-1]


    def terminate(self):
        if self.is_alive():
            self._alive = False
            super().terminate()

    # Make sure the process exits in case tracing fails
    def _run_bcc_trace(self):
        sys.argv = self._args
        try:
            Tool().run()
        finally:
            exit(1)
