'''
This module contains a collections of tools
used by different parts of the application.
'''
from collections import namedtuple
from operator import itemgetter
from pathlib import Path
from re import compile, match

import yaml


# Regex patterns to match in bcc trace output
FUNCTION_PATTERN = compile(r'^b\'(.+)\+.*\s\[(.+)\]')
PARAMS_PATTERN = compile(r'^\d+\s+\d+\s+\S+\s+\S+\s+(.+)')
OUTPUT_START = compile(r'^PID\s+TID\s+COMM\s+FUNC')
STACK_END_PATTERN = '---'


# Struct to contains a call-stack from bcc trace output
Graph = namedtuple('Graph', 'nodes edges')


# Special exception class to handle all exceptions
# during processing functions to trace
class ProcessException(Exception):
    pass


# Format specifiers and their labels to show for parameters
def format_specs():
    return [
        ('char', '%c'),
        ('double/float', '%f'),
        ('int', '%d'),
        ('long', '%l'),
        ('long double', '%lF'),
        ('string/char *', '%s'),
        ('short', '%hi'),
        ('unsigned short', '%hi'),
        ('void *', '%p'),
    ]


# Convert dictionary of functions to trace into
# properly structured list to be used by the trace command
def flatten_trace_dict(trace_dict):
    def params_to_ordered_list_of_pairs(params):
        param_list = [(param, params[param]) for param in params]
        param_list.sort(key=itemgetter(0))
        return param_list

    trace_list = []
    for app in trace_dict:
        functions = trace_dict[app]
        for function in functions:
            func_formula = '{}:{}'.format(app, function)
            params = trace_dict[app][function]
            if params:
                param_list = params_to_ordered_list_of_pairs(params)
                func_formula = '{} "{}", {}'.format(
                    func_formula,
                    ' '.join([param[1] for param in param_list]),
                    ', '.join([param[0] for param in param_list]))
            trace_list.append(func_formula)

    if not trace_list:
        raise ProcessException('No functions to trace')
    return trace_list


# Parse bcc trace output by processing it line by line
# Working always with two neighbouring lines at a time (except for the first)
# where the former is considered the called function
# and the latter is considered the caller function
def parse_stack(stack):
    # Create node for a function with its name and source
    def create_node(regex):
        node_dict = {}
        node_dict['name'] = regex.group(1)
        node_dict['source'] = regex.group(2)
        return node_dict

    # Create hash based on the name and source of function
    def create_hash_for_node(node_dict):
        return str(hash(frozenset(node_dict.items())))

    # Add edge to the edges to be returned
    def expand_edges(called, caller, edges, params, traced):
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
    def expand_nodes(node_dict, node_hash, nodes, called):
        # If the node is not already present then add it to the list
        if node_hash not in nodes:
            nodes[node_hash] = node_dict
            nodes[node_hash]['call_count'] = 0
        # If the function is at the top of the call-stack then increase call count
        if not called:
            nodes[node_hash]['call_count'] += 1

    # Get parameters from a single stack
    def get_params(header):
        params = PARAMS_PATTERN.match(header)
        if params:
            return [param.lstrip('b').strip("'") for param in params.group(1).rstrip('\r').split(' ') if param != '']
        return None

    if not stack:
        return Graph(nodes={}, edges={})


    if OUTPUT_START.match(stack[0]):
        stack.pop(0)
    if not stack:
        return Graph(nodes={}, edges={})

    params = get_params(stack.pop(0))

    nodes = {}
    edges = {}
    called_hash = None
    traced = True
    while stack:
        call = stack.pop(0)
        caller = FUNCTION_PATTERN.match(call)
        if caller:
            caller_node = create_node(caller)
            caller_hash = create_hash_for_node(caller_node)
            expand_nodes(caller_node, caller_hash, nodes, called_hash)
            if called_hash:
                expand_edges(called_hash, caller_hash, edges, params, traced)
                params = None
                traced = False
            called_hash = caller_hash
    return Graph(nodes=nodes, edges=edges)


# Split raw text into list of stacks
def text_to_stacks(text):
    return [stack.split('\n') for stack in text.split('\n\n')]


# Parse config file containing funtions to trace
def extract_config(config_path):
    try:
        path = Path(config_path)
    except TypeError:
        raise ProcessException('Please provide a path to the configuration file')

    try:
        content = yaml.safe_load(path.read_text())
    except yaml.scanner.ScannerError:
        raise ProcessException('Config file at {} has to be YAML format'.format(str(config_path)))
    except FileNotFoundError:
        raise ProcessException('Could not find configuration file at {}'.format(str(config_path)))
    except IsADirectoryError:
        raise ProcessException('{} is a directory, not a file'.format(str(config_path)))
    except Exception:
        raise ProcessException('Unknown error happened while processing config file')

    trace_list = []

    try:
        for app in content:
            for func in content[app]:
                if isinstance(func, dict):
                    params_specs = list(func.values())[0]
                    func_formula = '{}:{} "{}", {}'.format(
                        app,
                        list(func.keys())[0],
                        ' '.join(params_specs),
                        ', '.join(['arg{}'.format(i+1) for i in range(len(params_specs))]))
                else:
                    func_formula = '{}:{}'.format(app, func)
                trace_list.append(func_formula)
    except TypeError:
        raise ProcessException('Could not process configuration file')

    if not trace_list:
        raise ProcessException('No functions to trace')
    return trace_list
