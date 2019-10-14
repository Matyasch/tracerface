from queue import Queue, Empty
import subprocess
import threading

import pexpect

from parser import text_to_stacks, process_stack

# Manages logic and persistence
class Model:
    def __init__(self, persistence):
        self.persistence = persistence
        self.thread = threading.Thread()
        self.thread_enabled = False

    # Returns a list of nodes and their call count
    def get_nodes(self):
        return self.persistence.nodes

    # Returns a list of edges and their frequency
    def get_edges(self):
        return self.persistence.edges

    def yellow_count(self):
        return self.persistence.get_range().yellow

    def red_count(self):
        return self.persistence.get_range().red

    def max_count(self):
        return self.persistence.get_range().top

    def initialize_from_text(self, raw_text):
        self.persistence.clear()
        stacks = text_to_stacks(raw_text)
        for stack in stacks:
            graph = process_stack(stack)
            self.persistence.load_edges(graph.edges)
            self.persistence.load_nodes(graph.nodes)
        self.persistence.init_colors()

    def run_command(self, cmd):
        child = pexpect.spawn(cmd, timeout=None)
        stack = []
        while self.thread_enabled:
            try:
                child.expect('\n')
                raw = child.before
                call = raw.decode("utf-8")
                if call == '\r':
                    graph = process_stack(stack)
                    self.persistence.load_edges(graph.edges)
                    self.persistence.load_nodes(graph.nodes)
                    stack.clear()
                else:
                    stack.append(call)
            except pexpect.EOF:
                break
        child.close()

    def start_trace(self, functions):
        self.persistence.clear()
        cmd = ['trace-bpfcc', '-UK'] + functions
        self.thread_enabled = True
        thread = threading.Thread(target=self.run_command, args=[' '.join(cmd)])
        thread.start()

    def stop_trace(self):
        self.thread_enabled = False
        self.persistence.init_colors()

    def set_range(self, yellow, red):
        self.persistence.update_color_range(yellow, red)