from collections import namedtuple
import operator

Range = namedtuple('Range', 'yellow red top')

class Persistence:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.yellow = 0
        self.red = 0

    def load_nodes(self, nodes):
        for node in nodes:
            if node in self.nodes:
                self.nodes[node]['call_count'] += nodes[node]['call_count']
            else:
                self.nodes[node] = nodes[node]
        self.init_colors()

    def load_edges(self, edges):
        for edge in edges:
            if edge in self.edges:
                if edges[edge]['param']:
                    self.edges[edge]['params'].append(edges[edge]['param'])
                    self.edges[edge]['call_count'] += edges[edge]['call_count']
            else:
                self.edges[edge] = {}
                self.edges[edge]['params'] = []
                if edges[edge]['param']:
                    self.edges[edge]['params'].append(edges[edge]['param'])
                self.edges[edge]['call_count'] = edges[edge]['call_count']

    def clear(self):
        self.nodes = {}
        self.edges = {}

    def max_calls(self):
        if self.nodes:
            return max([node['call_count'] for node in self.nodes.values()])
        return 0

    def init_colors(self):
        self.yellow=round(self.max_calls()/3)
        self.red=round(self.max_calls()*2/3)

    def update_color_range(self, yellow, red):
        self.yellow = yellow
        self.red = red

    def get_range(self):
        return Range(
            yellow=self.yellow,
            red=self.red,
            top=self.max_calls()
        )