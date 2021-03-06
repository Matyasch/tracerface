from dash_bootstrap_components import Col, Row
from dash_html_components import Div

from tracerface.web_ui.dashboard import Dashboard
from .graph import Graph


# Implementation of the base layout of the user interface
class Layout(Div):
    def __init__(self):
        super().__init__(
            children=Row([
                Col(Graph()),
                Col(Dashboard(), width=3)
            ]),
            style={'width': '99vw'},)
