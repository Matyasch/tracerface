from queue import Queue, Empty
import subprocess
import threading

import pexpect

from parser import Graph, Parser

# Manages logic and persistence
class Model:
    def __init__(self, persistence):
        self.persistence = persistence
        self.parser = Parser()
        self.thread = threading.Thread()
        self.thread_enabled = False

    # Returns a list of nodes and their call count
    def get_nodes(self):
        return self.persistence.nodes

    # Returns a list of edges and their frequency
    def get_edges(self):
        return self.persistence.edges

    def green_count(self):
        return 0

    def yellow_count(self):
        return int(self.persistence.get_max_calls()/3)

    def red_count(self):
        return int(self.persistence.get_max_calls()*2/3)

    def initialize_from_text(self, raw_text):
        self.persistence.clear()
        stacks = self.parser.parse_text_to_stack_list(raw_text)
        for stack in stacks:
            graph = self.parser.process_call_stack(stack)
            self.persistence.load_edges(graph.edges)
            self.persistence.load_nodes(graph.nodes)

    def run_command(self, cmd):
        child = pexpect.spawn(cmd, timeout=None)
        stack = []
        while self.thread_enabled:
            try:
                child.expect('\n')
                raw = child.before
                call = raw.decode("utf-8")
                if call == '\r':
                    graph = self.parser.process_call_stack(stack)
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