from threading import Thread

from tracerface.parse_stack import parse_stack
from tracerface.trace_process import TraceProcess


# The TraceController class manages the lifecycle
# of the tracing process, consumes and parses its
# outputs, and loads them into the given CallGraph
class TraceController:
    def __init__(self):
        self._thread_enabled = False
        self._thread_error = None

    # While tracing, consume items from the queue and process them
    def _monitor_tracing(self, trace_process, call_graph):
        calls = []
        last_line_was_empty = False # call-stack ends when two empty lines follow eachother
        while self._thread_enabled:
            # If process died unexpectedly, report error
            if not trace_process.is_alive():
                self._thread_error = 'Tracing stopped unexpectedly'
                break
            output = trace_process.get_output()
            # call-stack ended
            if output == '\n' and last_line_was_empty:
                stack = parse_stack(calls)
                call_graph.load_edges(stack.edges)
                call_graph.load_nodes(stack.nodes)
                call_graph.init_colors()
                calls.clear()
            # new line after a regular output
            elif output == '\n':
                last_line_was_empty = True
            # regular output from bcc trace
            elif output:
                last_line_was_empty = False
                calls.append(output)
        # Terminate process when tracing is stopped by the user
        if trace_process.is_alive():
            trace_process.terminate()
            trace_process.join()

    # Starts tracing of given functions
    def start_trace(self, functions, call_graph):
        if not functions:
            self._thread_error = 'No functions to trace'
            return
        self._thread_error = None
        self._thread_enabled = True

        args = ['', '-UK'] + [fr'{function}' for function in functions]
        trace_process = TraceProcess(args=args)
        monitoring = Thread(target=self._monitor_tracing, args=(trace_process, call_graph,))
        trace_process.start()
        monitoring.start()

    # Stop tracing and initialize colors
    def stop_trace(self):
        self._thread_enabled = False

    # Returns error happening while an active trace
    def thread_error(self):
        return self._thread_error
