import dash_bootstrap_components as dbc
import dash_html_components as html

from view.info_card import InfoCard
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
        self.info_card = InfoCard(view_model)

    def dashboard(self):
        return html.Div(
            id='dashboard',
            children=[
                dbc.Tabs(
                    id='tabs',
                    children=[
                        dbc.Tab(label='Realtime', tab_id='realtime-tab', id='realtime-tab', children=[self.realtime.tab()], tab_style={"margin-left": "auto"}),
                        dbc.Tab(label='Static', tab_id='static-tab', id='static-tab', children=[self.static.tab()]),
                        dbc.Tab(label='Utilities', tab_id='utilities-tab', id='utilities-tab', children=[self.utilities.tab()]),
                        dbc.Tab(label='Configure', tab_id='configure-tab', id='configure-tab', children=[self.configure.tab()]),
                    ]
                ),
                html.Div(children=[], id='info-card')])