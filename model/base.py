'''
Parent class of the two types of models used.
Provides basic functionality and persistence handling.
'''
from collections import namedtuple
from re import compile

from persistence.persistence import Persistence


# Regex patterns to match in bcc trace output
FUNCTION_PATTERN = compile(r'^b\'(.+)\+.*\s\[(.+)\]')
PARAMS_PATTERN = compile(r'^\d+\s+\d+\s+\S+\s+\S+\s+(.+)')
HEADER_PATTERN = compile(r'^PID\s+TID\s+COMM\s+FUNC')


# Struct to contains a call-stack from bcc trace output
Stack = namedtuple('Stack', 'nodes edges')


class BaseModel:
    def __init__(self):
        self._persistence = Persistence()

    # returns all nodes in a list
    def get_nodes(self):
        return self._persistence.get_nodes()

    # returns all edges in a list
    def get_edges(self):
        return self._persistence.get_edges()

    # returns the lower bound for coloring elements yellow
    def yellow_count(self):
        return self._persistence.get_yellow()

    # returns the lower bound for coloring elements red
    def red_count(self):
        return self._persistence.get_red()

    # returns the maximum number of calls among nodes
    def max_count(self):
        call_counts = [node['call_count'] for node in self._persistence.get_nodes().values()]
        if call_counts:
            return max(call_counts)
        return 0

    # set new values for the coloring bounds
    def set_range(self, yellow, red):
        self._persistence.update_colors(yellow, red)

    # initialize color boundaries to default values based on maximum count
    def init_colors(self):
        yellow = round(self.max_count()/3)
        red = round(self.max_count()*2/3)
        self._persistence.update_colors(yellow, red)

    # Parse bcc trace output by processing it line by line
    # Working always with two neighbouring lines at a time (except for the first)
    # where the former is considered the called function
    # and the latter is considered the caller function
    @staticmethod
    def parse_stack(stack):
        # Create node for a function with its name and source
        def create_node(regex):
            node_dict = {}
            node_dict['name'] = regex.group(1)
            node_dict['source'] = regex.group(2)
            return node_dict

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
            return Stack(nodes={}, edges={})

        if HEADER_PATTERN.match(stack[0]):
            stack.pop(0)
        if not stack:
            return Stack(nodes={}, edges={})

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
                caller_hash = str(hash(frozenset(caller_node.items())))
                expand_nodes(caller_node, caller_hash, nodes, called_hash)
                if called_hash:
                    expand_edges(called_hash, caller_hash, edges, params, traced)
                    params = None
                    traced = False
                called_hash = caller_hash
        return Stack(nodes=nodes, edges=edges)
