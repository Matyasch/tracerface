import sys
import re
from pathlib import Path

FUNCTION_PATTERN = '^\s+(.+)\+.*\s\[(.+)\]'

class Parser:
    def __init__(self):
        self.edges = {}
        self.nodes = {}

    def expand_edges(self, called, caller):
        if called:
            edge = (called.group(1), caller.group(1))
            if edge in self.edges:
                self.edges[edge] +=1
            else:
                self.edges[edge] = 1

    def expand_nodes(self, called, caller):
        caller_name = caller.group(1)
        if caller_name not in self.nodes:
            self.nodes[caller_name] = 0
        if not called:
            self.nodes[caller_name] += 1

    def process_call_list(self, calls):
        called = None
        for call in calls:
            caller = re.search(FUNCTION_PATTERN, call)
            if caller:
                self.expand_edges(called, caller)
                self.expand_nodes(called, caller)
                called = caller

    def parse_from_text(self, output):
        stacks = output.split('\n\n')
        for stack in stacks:
            calls = stack.split('\n')
            self.process_call_list(calls)

    def parse_from_list(self, stack):
        self.process_call_list(stack)