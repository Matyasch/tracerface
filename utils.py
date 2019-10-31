from collections import namedtuple
import re

def c_type_pairs():
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
    trace_list = []
    for app in trace_dict:
        functions = trace_dict[app]
        for function in functions:
            func_formula = '{}:{}'.format(app, function)
            params = trace_dict[app][function]
            if params:
                func_formula = '{} "{}", {}'.format(
                    func_formula,
                    ' '.join([trace_dict[app][function][param] for param in params]),
                    ', '.join([param for param in params]))
            trace_list.append(func_formula)
    return trace_list

def parse_stack(stack):
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