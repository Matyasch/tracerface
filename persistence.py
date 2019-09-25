import operator

class Persistence:
    def load_nodes(self, nodes):
        self.nodes = nodes
        self.max_count = nodes[max(nodes.items(), key=operator.itemgetter(1))[0]]

    def load_edges(self, edges):
        self.edges = edges