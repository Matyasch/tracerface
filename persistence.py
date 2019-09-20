class Persistence:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def load(self, parsed_output):
        self.edges = set(tuple(edge) for edge in parsed_output)
        for edge in self.edges:
            self.nodes.append(edge[0])
        self.nodes = list(set(self.nodes))