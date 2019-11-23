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

    def max_calls(self):
        if self._nodes:
            return max([node['call_count'] for node in self._nodes.values()])
        return 0

    def init_colors(self):
        self._yellow=round(self.max_calls()/3)
        self._red=round(self.max_calls()*2/3)

    def update_color_range(self, yellow, red):
        self._yellow = yellow
        self._red = red

    def get_yellow(self):
        return self._yellow

    def get_red(self):
        return self._red

    def get_top(self):
        return self.max_calls()