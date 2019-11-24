class Persistence:
    def __init__(self):
        self._nodes = {}
        self._edges = {}
        self._yellow = 0
        self._red = 0

    def load_nodes(self, nodes):
        for node in nodes:
            if node in self._nodes:
                self._nodes[node]['call_count'] += nodes[node]['call_count']
            else:
                self._nodes[node] = nodes[node]

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

    def get_nodes(self):
        return self._nodes

    def get_edges(self):
        return self._edges

    def clear(self):
        self._nodes = {}
        self._edges = {}

    def update_colors(self, yellow, red):
        self._yellow = yellow
        self._red = red

    def get_yellow(self):
        return self._yellow

    def get_red(self):
        return self._red