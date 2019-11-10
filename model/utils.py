from collections import namedtuple
from operator import itemgetter
from pathlib import Path
import re

import yaml

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
    return trace_list

def parse_stack(stack):
    FUNCTION_PATTERN = '^\s+(.+)\+.*\s\[(.+)\]'
    PARAMS_PATTERN = '^\d+\s+\d+\s+\S+\s+\S+\s+(.+)'
    OUTPUT_START = '^PID\s+TID\s+COMM\s+FUNC'

    Graph = namedtuple('Graph', 'nodes edges')

    def create_node(regex):
        node_dict = {}
        node_dict['name'] = regex.group(1)
        node_dict['source'] = regex.group(2)
        return node_dict

    def create_hash_for_node(node_dict):
        return str(hash(frozenset(node_dict.items())))

    def expand_edges(called, caller, edges, params, traced):
        edge_id = (caller, called)
        if edge_id not in edges:
            edges[edge_id] = {}
            edges[edge_id]['param'] = params
            edges[edge_id]['call_count'] = 0
        if traced:
            edges[edge_id]['call_count'] += 1

    def expand_nodes(node_dict, node_hash, nodes, called):
        if node_hash not in nodes:
            nodes[node_hash] = node_dict
            nodes[node_hash]['call_count'] = 0
        if not called:
            nodes[node_hash]['call_count'] += 1

    def get_params(header):
        params = re.search(PARAMS_PATTERN, header)
        if params:
            return [param for param in params.group(1).rstrip('\r').split(' ') if param != '']
        return None

    nodes = {}
    edges = {}

    if re.search(OUTPUT_START, stack[0]):
        stack.pop(0)
    params = get_params(stack.pop(0))

    called_hash = None
    traced = True
    for call in stack[1:]:
        caller = re.search(FUNCTION_PATTERN, call)
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

def text_to_stacks(text):
    return [stack.split('\n') for stack in text.split('\n\n')]

def extract_config(config_path):
    path = Path(config_path)
    content = yaml.safe_load(path.read_text())
    trace_list = []
    for app in content:
        for func in content[app]:
            if isinstance(func, dict):
                params_specs = list(func.values())[0]
                func_formula = '{}:{} "{}", {}'.format(
                    app,
                    list(func.keys())[0],
                    ' '.join(params_specs),
                    ', '.join(['arg{}'.format(i+1) for i in range(len(params_specs))])
                )
            else:
                func_formula = '{}:{}'.format(app, func)
            trace_list.append(func_formula)
    return trace_list