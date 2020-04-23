from dash_cytoscape import Cytoscape, load_extra_layouts

from view.styles import edge_styles, node_styles


# Implementation of the displayed graph
class Graph(Cytoscape):
    def __init__(self):
        load_extra_layouts()
        super().__init__(
            id='graph',
            layout=self.layout(),
            style={'height': '99vh'},
            elements=[],
            stylesheet=self.stylesheet())

    @staticmethod
    def stylesheet(search='', yellow_count=0, red_count=0):
        return node_styles(yellow_count, red_count, search) + edge_styles(yellow_count, red_count, search)

    @staticmethod
    def layout(spacing=2, animate=False):
        return {
            'name': 'dagre',
            'spacingFactor': spacing,
            'animate': animate
        }
