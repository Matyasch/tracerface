from dash_bootstrap_components import Tab, Tabs
from dash_html_components import Div, Hr

from view.configure_tab import ConfigureTab
from view.static_tab import StaticTab
from view.realtime_tab import RealtimeTab
from view.utilities_tab import UtilitiesTab


class Dashboard:
    def __init__(self, view_model):
        self.view_model = view_model
        self.configure = ConfigureTab()
        self.static = StaticTab()
        self.realtime = RealtimeTab()
        self.utilities = UtilitiesTab(view_model)

    def dashboard(self):
        return Div(
            id='dashboard',
            children=[
                Tabs(
                    id='tabs',
                    children=[
                        Tab(label='Realtime', tab_id='realtime-tab', id='realtime-tab', children=[self.realtime.tab()], tab_style={"margin-left": "auto"}),
                        Tab(label='Static', tab_id='static-tab', id='static-tab', children=[self.static.tab()]),
                        Tab(label='Utilities', tab_id='utilities-tab', id='utilities-tab', children=[self.utilities.tab()]),
                        Tab(label='Configure', tab_id='configure-tab', id='configure-tab', children=[self.configure.tab()])]),
                Hr(),
                Div(children=[], id='info-card')])