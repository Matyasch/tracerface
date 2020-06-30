#!/usr/bin/env python3

# Representation of the call graph
# generated through the tracing
class CallGraph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}
        self._yellow = 0
        self._red = 0

    # Merge collection of new nodes to already existing ones
    def load_nodes(self, nodes):
        for node in nodes:
            if node in self._nodes:
                self._nodes[node]['call_count'] += nodes[node]['call_count']
            else:
                self._nodes[node] = nodes[node]

    # Merge collection of new edges to already existing ones
    def load_edges(self, edges):
        for edge in edges:
            if edge in self._edges:
                self._edges[edge]['call_count'] += edges[edge]['call_count']
                if edges[edge]['param']:
                    self._edges[edge]['params'].append(edges[edge]['param'])
            else:
                self._edges[edge] = {}
                self._edges[edge]['params'] = []
                self._edges[edge]['call_count'] = edges[edge]['call_count']
                if edges[edge]['param']:
                    self._edges[edge]['params'].append(edges[edge]['param'])

    # Return list of all nodes
    def get_nodes(self):
        return self._nodes

    # Return list of all edges
    def get_edges(self):
        return self._edges

    # Clear nodes and edges from graph
    def clear(self):
        self._nodes = {}
        self._edges = {}
        self._yellow = 0
        self._red = 0

    # Set bounds for yellow and red coloring
    def set_colors(self, yellow, red):
        self._yellow = yellow
        self._red = red

    # Return lower bound of call count to color with yellow
    def get_yellow(self):
        return self._yellow

    # Return lower bound of call count to color with red
    def get_red(self):
        return self._red

    # returns the maximum number of calls among nodes
    def max_count(self):
        call_counts = [node['call_count'] for node in self._nodes.values()]
        if call_counts:
            return max(call_counts)
        return 0

    # initialize color boundaries to default values based on maximum count
    def init_colors(self):
        max_count = self.max_count()
        new_yellow = round(max_count / 3)
        new_red = new_yellow * 2
        self.set_colors(new_yellow, new_red)
