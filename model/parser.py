from collections import namedtuple
from pathlib import Path
import re
import sys

FUNCTION_PATTERN = '^\s+(.+)\+.*\s\[(.+)\]'
PARAMS_PATTERN = '^\d+\s+\d+\s+\S+\s\S+\s+(.+)'

Graph = namedtuple('Graph', 'nodes edges')

def expand_edges(called, caller, edges, params):
    if called:
        edge = (called.group(1), caller.group(1))
        if edge in edges:
            pass
        else:
            edges[edge] = {}
            edges[edge]['param'] = params
def expand_nodes(called, caller, nodes):
    caller_name = caller.group(1)
    if caller_name not in nodes:
        nodes[caller_name] = {}
        nodes[caller_name]['call_count'] = 0
    if not called:
        nodes[caller_name]['call_count'] += 1

def get_params(header):
    params = re.search(PARAMS_PATTERN, header)
    if params:
        params = params.group(1).rstrip('\r').split(' ')
    return params if params != [''] else None

def process_stack(stack):
    nodes = {}
    edges = {}
    called = None
    params = get_params(stack[0])
    for call in stack[1:]:
        caller = re.search(FUNCTION_PATTERN, call)
        if caller:
            expand_edges(called, caller, edges, params)
            expand_nodes(called, caller, nodes)
            if called:
                params = None
            called = caller
    return Graph(nodes=nodes, edges=edges)

def text_to_stacks(text):
    return [stack.split('\n') for stack in text.split('\n\n')]