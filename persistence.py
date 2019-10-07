import operator

class Persistence:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def load_nodes(self, nodes):
        for node in nodes:
            if node in self.nodes:
                self.nodes[node] += nodes[node]
            else:
                self.nodes[node] = nodes[node]

    def load_edges(self, edges):
        self.edges = {**self.edges, **edges}

    def clear(self):
        self.nodes = {}
        self.edges = {}

    def get_max_calls(self):
        if self.nodes:
            return max(self.nodes.values())
        return 0