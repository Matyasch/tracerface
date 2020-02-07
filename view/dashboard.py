from dash_bootstrap_components import Tab, Tabs
from dash_html_components import Div, Hr

from view.static_tab import StaticTab
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
                        StaticTab(),
                        UtilitiesTab()]),
                Hr(),
                Div(children=[], id='info-card')])
