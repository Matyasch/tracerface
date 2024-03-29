#!/usr/bin/env python3
'''
Parse bcc trace output by processing it line by line.
Two neighbouring lines are considered at a time
where the former is the called function
and the latter is the caller function
'''
from collections import namedtuple
from hashlib import sha256
from re import compile


# Regex patterns to match in bcc trace output
_FUNCTION_PATTERN = compile(r'([a-zA-Z0-9_]+)\+.*\s\[(.+)\]')
_PARAMS_PATTERN = compile(r'^\d+\s+\d+\s+\S+\s+\S+\s+(.+)')
_HEADER_PATTERN = compile(r'^PID\s+TID\s+COMM\s+FUNC')


# Struct to contains a call-stack from bcc trace output
Stack = namedtuple('Stack', 'nodes edges')


# Create node for a function with its name and source
def _create_node(regex):
    node_dict = {}
    node_dict['name'] = regex.group(1)
    node_dict['source'] = regex.group(2)
    return node_dict


# Add edge to the edges to be returned
def _expand_edges(called, caller, edges, params, traced):
    edge_id = (caller, called)
    # If the edge is not already present then add it to the list
    if edge_id not in edges:
        edges[edge_id] = {}
        edges[edge_id]['param'] = params or []
        edges[edge_id]['call_count'] = 0
    # If the edge goes to a traced function then increase call count
    if traced:
        edges[edge_id]['call_count'] += 1


# Add node to the nodes to be returned
def _expand_nodes(node_dict, node_hash, nodes, called):
    # If the node is not already present then add it to the list
    if node_hash not in nodes:
        nodes[node_hash] = node_dict
        nodes[node_hash]['call_count'] = 0
    # If the function is at the top of the call-stack then increase call count
    if not called:
        nodes[node_hash]['call_count'] += 1


# Get parameters from a single stack
def _get_params(header):
    params = _PARAMS_PATTERN.match(header)
    if params:
        return [param.lstrip('b').strip("'") for param in params.group(1).rstrip('\r').split(' ') if param != '']
    return None


def parse_stack(stack):
    if not stack:
        return Stack(nodes={}, edges={})

    if _HEADER_PATTERN.match(stack[0]):
        stack.pop(0)
    if not stack:
        return Stack(nodes={}, edges={})

    params = _get_params(stack.pop(0))

    nodes = {}
    edges = {}
    called_hash = None
    traced = True
    while stack:
        call = stack.pop(0)
        caller = _FUNCTION_PATTERN.search(call)
        if caller:
            caller_node = _create_node(caller)
            caller_hash = sha256(repr(caller_node).encode()).hexdigest()
            _expand_nodes(caller_node, caller_hash, nodes, called_hash)
            if called_hash:
                _expand_edges(called_hash, caller_hash, edges, params, traced)
                params = None
                traced = False
            called_hash = caller_hash
    return Stack(nodes=nodes, edges=edges)
