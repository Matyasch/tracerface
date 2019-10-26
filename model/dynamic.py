import threading

import pexpect

from model.base import BaseModel
from parser import process_stack

# Manages logic and persistence
class DynamicModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._thread = threading.Thread()
        self._thread_enabled = False

    def _run_command(self, cmd):
        child = pexpect.spawn(cmd, timeout=None)
        stack = []
        while self._thread_enabled:
            try:
                child.expect('\n')
                raw = child.before
                call = raw.decode("utf-8")
                if call == '\r':
                    graph = process_stack(stack)
                    self._persistence.load_edges(graph.edges)
                    self._persistence.load_nodes(graph.nodes)
                    stack.clear()
                else:
                    stack.append(call)
            except pexpect.EOF:
                break
        child.close()

    def start_trace(self, functions):
        self._persistence.clear()
        cmd = [self._configuration.bcc_command, '-UK'] + functions
        self._thread_enabled = True
        thread = threading.Thread(target=self._run_command, args=[' '.join(cmd)])
        thread.start()

    def stop_trace(self):
        self._thread_enabled = False
        self._persistence.init_colors()