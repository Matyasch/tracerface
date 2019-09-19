class Data:
    def __init__(self, parsed_output):
        self.nodes = []
        self.edges = set(tuple(edge) for edge in parsed_output)
        for edge in self.edges:
            self.nodes.append(edge[0])
        self.nodes = list(set(self.nodes))