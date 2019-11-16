from dash_bootstrap_components import Col, Row
from dash_html_components import Div

from view.dashboard import Dashboard
from view.graph import Graph
import view.styles as styles


class Layout:
    def layout(self):
        return Div(Row([
            Col(Graph(), width=9),
            Col(Dashboard())],
            style={'width': '100%'}))