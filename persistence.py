import operator

class Persistence:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.max_count = 0

    def load_nodes(self, nodes):
        self.nodes = {**self.nodes, **nodes}
        if self.nodes:
            self.max_count = self.nodes[max(self.nodes.items(), key=operator.itemgetter(1))[0]]

    def load_edges(self, edges):
        self.edges = {**self.edges, **edges}