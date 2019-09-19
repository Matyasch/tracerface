class Data:
    def __init__(self):
        self.nodes = []
        self.edges = []
        with open("assets/data") as infile:
            for line in infile:
                elements = line.rstrip('\n').split(' ')
                self.nodes.append(elements[0])
                self.edges.append(elements)
        self.nodes = list(set(self.nodes))