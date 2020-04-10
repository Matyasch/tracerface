from multiprocessing import Queue
from pathlib import Path
from queue import Empty
from threading import Thread
import yaml

from model.base import BaseModel
from model.parse_stack import parse_stack
from model.trace_utils import TraceProcess, STACK_END_PATTERN


# Special exception class to handle all exceptions
# during processing functions to trace
class ProcessException(Exception):
    pass


# Model for tracing realtime
class DynamicModel(BaseModel):
    def __init__(self, persistence):
        super().__init__(persistence)
        self._thread_enabled = False
        self._thread_error = None
        self._process_error = None

    # Start tracing with the functions given in a configuration file
    def trace_yaml(self, config_path):
        try:
            functions = self.parse_args_from_file(config_path)
            self.start_trace(functions)
        except ProcessException as e:
            self._process_error = str(e)

    # While tracing, consume items from the queue and process them
    def monitor_tracing(self, queue, process):
        calls = []
        while self._thread_enabled:
            # If process died unexpectedly, report error
            if not process.is_alive():
                self._thread_error = 'Tracing stopped unexpectedly'
                break
            try:
                # Get only one item at a time from the queue, in case
                # tracing gets stopped but queue keeps getting items
                # so we keep checking the loop condition.
                output = queue.get_nowait()
                if output == STACK_END_PATTERN:
                    stack = parse_stack(calls)
                    self._persistence.load_edges(stack.edges)
                    self._persistence.load_nodes(stack.nodes)
                    self.init_colors()
                    calls.clear()
                else:
                    calls.append(output)
            except Empty:
                pass
        # If tracing was stopped by the user, terminate tracing process
        if(process.is_alive()):
            process.terminate()
            process.join()

    # Clear errors and persistence, initialize values needed for tracing,
    # build argument list then start tracing and monitoring its output
    def start_trace(self, functions):
        self._thread_error = None
        self._thread_enabled = True
        self._persistence.clear()

        args = ['', '-UK'] + [fr'{function}' for function in functions]
        queue = Queue()
        trace_process = TraceProcess(queue=queue, args=args)
        monitoring = Thread(target=self.monitor_tracing, args=[queue, trace_process])
        print(args)
        trace_process.start()
        monitoring.start()

    # Stop tracing and initialize colors
    def stop_trace(self):
        self._thread_enabled = False
        self.init_colors()

    # Returns error happening while an active trace
    def thread_error(self):
        return self._thread_error

    # Returns error happening during the procession of functions to trace
    def process_error(self):
        return self._process_error

    # Returns status wether tracing is currently active or not
    def trace_active(self):
        return self._thread_enabled
