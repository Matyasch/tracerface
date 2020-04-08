from dash_bootstrap_components import Col, Row

from view.dashboard import Dashboard
from view.graph import Graph


# Implementation of the base layout of the user interface
class Layout(Row):
    def __init__(self):
        super().__init__([
            Col(Graph(), width=9),
            Col(Dashboard())
        ])
