import threading

import pexpect

from model.base import BaseModel
from utils import (
    extract_config,
    flatten_trace_dict,
    parse_stack
)

# Manages logic and persistence
class DynamicModel(BaseModel):
    def __init__(self, configuration):
        super().__init__(configuration)
        self._thread = threading.Thread()
        self._thread_enabled = False
        self._thread_error = None

    def _run_command(self, cmd):
        self._thread_error = None
        try:
            child = pexpect.spawn(cmd, timeout=None)
            stack = []
            while self._thread_enabled:
                try:
                    child.expect('\n')
                    raw = child.before
                    call = raw.decode("utf-8")
                    if call == '\r':
                        graph = parse_stack(stack)
                        self._persistence.load_edges(graph.edges)
                        self._persistence.load_nodes(graph.nodes)
                        stack.clear()
                    else:
                        stack.append(call)
                except pexpect.EOF:
                    self._thread_enabled = False
            child.close()
        except pexpect.exceptions.ExceptionPexpect as e:
            self._thread_error = str(e)

    def trace_dict(self, dict_to_trace):
        self._persistence.clear()
        functions = flatten_trace_dict(dict_to_trace)
        cmd = [self._configuration.bcc_command, '-UK'] + ['\'{}\''.format(function) for function in functions]
        self.debug = ' '.join(cmd)
        self._thread_enabled = True
        thread = threading.Thread(target=self._run_command, args=[' '.join(cmd)])
        thread.start()

    def trace_config_file(self, config_path):
        self._persistence.clear()
        functions = extract_config(config_path)
        cmd = [self._configuration.bcc_command, '-UK'] + ['\'{}\''.format(function) for function in functions]
        self._thread_enabled = True
        thread = threading.Thread(target=self._run_command, args=[' '.join(cmd)])
        thread.start()

    def stop_trace(self):
        self._thread_enabled = False
        self._persistence.init_colors()

    def trace_error(self):
        return self._thread_error

    def trace_active(self):
        return self._thread_enabled