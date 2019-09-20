class Persistence:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def load(self, parsed_output):
        self.edges = set(tuple(edge) for edge in parsed_output)