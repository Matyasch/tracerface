from dash_cytoscape import Cytoscape, load_extra_layouts

import view.styles as styles


# Implementation of the displayed graph
class Graph(Cytoscape):
    def __init__(self):
        load_extra_layouts()
        super().__init__(
            id='graph',
            layout=self.layout(),
            style={'height': '100vh'},
            elements=[],
            stylesheet=self.stylesheet())

    @staticmethod
    def stylesheet(search='', yellow_count=0, red_count=0):
        if not search:
            search=''
        return [
            styles.base_node_style(),
            styles.green_node_style(yellow_count, search),
            styles.yellow_node_style(yellow_count, red_count, search),
            styles.red_node_style(red_count, search),
            styles.base_edge_style(),
            styles.green_edge_style(yellow_count, search),
            styles.yellow_edge_style(yellow_count, red_count, search),
            styles.red_edge_style(red_count, search)
        ]

    @staticmethod
    def layout(spacing=2, animate=False):
        return {
            'name': 'dagre',
            'spacingFactor': spacing,
            'animate': animate
        }
