from dash_bootstrap_components import Col, Row
from dash_html_components import Div

from view.dashboard import Dashboard
from view.graph import Graph
import view.styles as styles


class Layout:
    def __init__(self, view_model):
        self.graph = Graph(view_model)

    def graph_div(self):
        return Div(
            id='graph-div',
            children=self.graph.graph())

    def layout(self):
        return Div(Row([
            Col(self.graph_div(), width=9),
            Col(Dashboard())],
            style={'width': '100%'}))