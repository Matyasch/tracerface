import json

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

class WebApp:
    def __init__(self, view):
        self.app = dash.Dash(__name__)
        self.app.layout = view.app_layout()