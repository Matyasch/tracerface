import sys
import re
from pathlib import Path

FUNCTION_PATTERN = '^\s+(.+)\+.*\s\[(.+)\]$'

class Parser:
    def __init__(self):
        self.edges = {}
        self.nodes = {}

    def get_edges_from_stack(self, calls):
        called = None
        for call in calls:
            caller = re.search(FUNCTION_PATTERN, call)
            if caller:
                caller_name = caller.group(1)
                if caller_name not in self.nodes:
                    self.nodes[caller_name] = 0
                if called:
                    edge = (called.group(1), )
                    if edge in self.edges:
                        self.edges[(called.group(1), caller_name)] +=1
                    else:
                        self.edges[(called.group(1), caller_name)] = 1
                else:
                    self.nodes[caller_name] += 1
                called = caller

    def parse(self, output):
        stacks = output.split('\n\n')
        for stack in stacks:
            calls = stack.split('\n')
            self.get_edges_from_stack(calls)