from multiprocessing import Queue
from queue import Empty
from threading import Thread

from model.parse_stack import parse_stack
from model.trace_utils import TraceProcess, STACK_END_PATTERN


# Model for tracing and parsing the output
class Model:
    def __init__(self, persistence):
        self._persistence = persistence
        self._thread_enabled = False
        self._thread_error = None

    # returns all nodes in a list
    def get_nodes(self):
        return self._persistence.get_nodes()

    # returns all edges in a list
    def get_edges(self):
        return self._persistence.get_edges()

    # returns the lower bound for coloring elements yellow
    def yellow_count(self):
        return self._persistence.get_yellow()

    # returns the lower bound for coloring elements red
    def red_count(self):
        return self._persistence.get_red()

    # returns the maximum number of calls among nodes
    def max_count(self):
        call_counts = [node['call_count'] for node in self._persistence.get_nodes().values()]
        if call_counts:
            return max(call_counts)
        return 0

    # set new values for the coloring bounds
    def set_range(self, yellow, red):
        self._persistence.update_colors(yellow, red)

    # initialize color boundaries to default values based on maximum count
    def init_colors(self):
        yellow = round(self.max_count()/3)
        red = round(self.max_count()*2/3)
        self._persistence.update_colors(yellow, red)

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
        if not functions:
            self._thread_error = 'No functions to trace'
            return
        self._thread_error = None
        self._thread_enabled = True
        self._persistence.clear()

        args = ['', '-UK'] + [fr'{function}' for function in functions]
        queue = Queue()
        trace_process = TraceProcess(queue=queue, args=args)
        monitoring = Thread(target=self.monitor_tracing, args=[queue, trace_process])
        trace_process.start()
        monitoring.start()

    # Stop tracing and initialize colors
    def stop_trace(self):
        self._thread_enabled = False
        self.init_colors()

    # Returns error happening while an active trace
    def thread_error(self):
        return self._thread_error

    # Returns status wether tracing is currently active or not
    def trace_active(self):
        return self._thread_enabled

    def load_output(self, text):
        stacks = [stack.split('\n') for stack in text.split('\n\n')]
        for stack in stacks:
            graph = parse_stack(stack)
            self._persistence.load_edges(graph.edges)
            self._persistence.load_nodes(graph.nodes)
        self.init_colors()
