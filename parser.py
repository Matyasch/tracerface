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

    def process_call_list(self, calls, nodes, edges):
        called = None
        for call in calls:
            caller = re.search(FUNCTION_PATTERN, call)
            if caller:
                self.expand_edges(called, caller, edges)
                self.expand_nodes(called, caller, nodes)
                called = caller

    def parse_from_text(self, output):
        nodes = {}
        edges = {}
        stacks = output.split('\n\n')
        for stack in stacks:
            calls = stack.split('\n')
            self.process_call_list(calls, nodes, edges)
        return Graph(nodes=nodes, edges=edges)

    def parse_from_list(self, stack):
        nodes = {}
        edges = {}
        self.process_call_list(stack, nodes, edges)
        return Graph(nodes=nodes, edges=edges)