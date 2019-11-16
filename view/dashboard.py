from dash_bootstrap_components import Tab, Tabs
from dash_html_components import Div, Hr

from view.configure_tab import ConfigureTab
from view.static_tab import StaticTab
from view.realtime_tab import RealtimeTab
from view.utilities_tab import UtilitiesTab


class Dashboard:
    def __init__(self):
        self.configure = ConfigureTab()
        self.static = StaticTab()

    def dashboard(self):
        return Div(
            id='dashboard',
            children=[
                Tabs(
                    id='tabs',
                    children=[
                        RealtimeTab(),
                        Tab(label='Static', tab_id='static-tab', id='static-tab', children=[self.static.tab()]),
                        UtilitiesTab(),
                        Tab(label='Configure', tab_id='configure-tab', id='configure-tab', children=[self.configure.tab()])]),
                Hr(),
                Div(children=[], id='info-card')])