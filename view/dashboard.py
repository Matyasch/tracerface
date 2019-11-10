import dash_bootstrap_components as dbc
import dash_html_components as html

from view.info_card import InfoCard
from view.tabs import Tabs


class Dashboard:
    def __init__(self, view_model):
        self.view_model = view_model
        self.tabs = Tabs(view_model)
        self.info_card = InfoCard(view_model)

    def dashboard(self):
        return html.Div(
            id='dashboard',
            children=[
                dbc.Tabs(
                    id='tabs',
                    children=[
                        dbc.Tab(label='Realtime', tab_id='realtime-tab', id='realtime-tab', children=[self.tabs.realtime()], tab_style={"margin-left": "auto"}),
                        dbc.Tab(label='Static', tab_id='static-tab', id='static-tab', children=[self.tabs.static()]),
                        dbc.Tab(label='Utilities', tab_id='utilities-tab', id='utilities-tab', children=[self.tabs.utilities()]),
                        dbc.Tab(label='Configure', tab_id='configure-tab', id='configure-tab', children=[self.tabs.configure()]),
                    ]
                ),
                html.Div(children=[], id='info-card'),
                html.Div(children=[
                    html.P(
                        children=f'Info',
                        style={'margin-left': '3px'}
                    ),
                    html.Pre(
                        id='info-box',
                        style={
                            'border': 'thin lightgrey solid',
                            'overflowX': 'scroll'
                        }
                    )
                ])
            ]
        )