from dash_bootstrap_components import Tab, Tabs
from dash_html_components import Div, Hr

from view.configure_tab import ConfigureTab
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
                        UtilitiesTab(),
                        ConfigureTab()]),
                Hr(),
                Div(children=[], id='info-card')])
