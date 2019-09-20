import json

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

import view.layout as layout


class WebApp():
    def __init__(self, view_model):
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div([
            layout.graph_layout(view_model),
            layout.dashboard()
        ])