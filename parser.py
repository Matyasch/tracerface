from collections import namedtuple
from pathlib import Path
import re
import sys

FUNCTION_PATTERN = '^\s+(.+)\+.*\s\[(.+)\]'

Graph = namedtuple('Graph', 'nodes edges')

class Parser:
    def expand_edges(self, called, caller, edges):
        if called:
            edge = (called.group(1), caller.group(1))
            if edge in edges:
                edges[edge] +=1
            else:
                edges[edge] = 1

    def expand_nodes(self, called, caller, nodes):
        caller_name = caller.group(1)
        if caller_name not in nodes:
            nodes[caller_name] = 0
        if not called:
            nodes[caller_name] += 1

    def process_call_stack(self, stack):
        nodes = {}
        edges = {}
        called = None
        for call in stack:
            caller = re.search(FUNCTION_PATTERN, call)
            if caller:
                self.expand_edges(called, caller, edges)
                self.expand_nodes(called, caller, nodes)
                called = caller
        return Graph(nodes=nodes, edges=edges)

    def parse_text_to_stack_list(self, text):
        return [stack.split('\n') for stack in text.split('\n\n')]