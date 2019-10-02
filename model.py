from queue import Queue, Empty
import subprocess
import threading

import pexpect

from parser import Parser

# Manages logic and persistence
class Model:
    def __init__(self, persistence):
        self.persistence = persistence
        self.parser = Parser()
        self.thread = threading.Thread()

    # Returns a list of nodes and their call count
    def get_nodes(self):
        return self.persistence.nodes

    # Returns a list of edges and their frequency
    def get_edges(self):
        return self.persistence.edges

    def green_count(self):
        return 0

    def yellow_count(self):
        return int(self.persistence.max_count/3)

    def red_count(self):
        return int(self.persistence.max_count*2/3)

    def initialize_from_text(self, raw_text):
        self.parser.parse_from_text(raw_text)
        self.persistence.load_edges(self.parser.edges)
        self.persistence.load_nodes(self.parser.nodes)

    def run_command(self, cmd):
        child = pexpect.spawn(cmd, timeout=None)
        stack = []
        while True:
            try:
                child.expect('\n')
                call = child.before.decode("utf-8")
                if call == '\r':
                    self.parser.parse_from_list(stack)
                    self.persistence.load_edges(self.parser.edges)
                    self.persistence.load_nodes(self.parser.nodes)
                    stack.clear()
                else:
                    stack.append(call)
            except pexpect.EOF:
                break

    def start_trace(self, functions):
        cmd = ['trace-bpfcc', '-UK'] + functions
        thread = threading.Thread(target=self.run_command, args=[' '.join(cmd)])
        thread.start()