import sys
import re
from pathlib import Path

FUNCTION_PATTERN = '^\s+(.+)\+.*\s\[(.+)\]$'

class BccParser:
    def __init__(self):
        self.edges = {}
    def parse(self, output):
        stacks = output.split('\n\n')
        for stack in stacks:
            calls = stack.split('\n')
            self.get_edges_from_stack(calls)


    def get_edges_from_stack(self, calls):
        called = None
        for call in calls:
            caller = re.search(FUNCTION_PATTERN, call)
            if caller:
                if called:
                    edge = (called.group(1), caller.group(1))
                    if edge in self.edges:
                        self.edges[(called.group(1), caller.group(1))] +=1
                    else:
                        self.edges[(called.group(1), caller.group(1))] = 1
                called = caller