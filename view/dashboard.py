from dash_bootstrap_components import Tabs
from dash_html_components import Div, Hr

from view.realtime_tab import RealtimeTab
from view.utilities_tab import UtilitiesTab


# Implementation of the dasboard
class Dashboard(Div):
    def __init__(self):
        super().__init__(
            id='dashboard',
            children=[
                Tabs(
                    id='tabs',
                    children=[
                        RealtimeTab(),
                        UtilitiesTab()
                    ]),
                Hr(),
                Div(children=[], id='info-card')
            ])
