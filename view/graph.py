from dash_cytoscape import Cytoscape, load_extra_layouts

import view.styles as styles


class Graph:
    def __init__(self, view_model):
        self.view_model = view_model
        load_extra_layouts()

    def stylesheet(self, search=''):
        if not search:
            search=''
        return [
            styles.base_node_style(),
            styles.green_node_style(self.view_model.yellow_count(), search),
            styles.yellow_node_style(self.view_model.yellow_count(), self.view_model.red_count(), search),
            styles.red_node_style(self.view_model.red_count(), search),
            styles.base_edge_style(),
            styles.green_edge_style(self.view_model.yellow_count(), search),
            styles.yellow_edge_style(self.view_model.yellow_count(), self.view_model.red_count(), search),
            styles.red_edge_style(self.view_model.red_count(), search)
        ]

    def layout(self):
        return {
            'name': 'dagre',
            'spacingFactor': self.view_model.spacing_config(),
            'animate': self.view_model.animate_config()
        }

    def graph(self):
        return [Cytoscape(
            id='graph',
            layout=self.layout(),
            style={'height': '100vh'},
            elements= self.view_model.get_nodes() + self.view_model.get_edges(),
            stylesheet=self.stylesheet())]