import dash_bootstrap_components as dbc
import dash_html_components as html

from view.tabs import Tabs


class Dashboard:
    def __init__(self, view_model):
        self.view_model = view_model
        self.tabs = Tabs(view_model)

    def info_card(self, header, infos, params):
        return dbc.Card([
            dbc.CardHeader(header),
            dbc.CardBody([html.P(info) for info in infos] + [
                dbc.ListGroup(
                    [dbc.ListGroupItem(', '.join(param)) for param in params],
                    className='scrollable',
                    style={'max-height': '200px'})
            ])],
            color='light',
            style={'margin': '20px'})

    def node_info_card_content(self, node):
        header = node['name']
        call_count = node['count']
        params = self.view_model.get_params_of_node(node['id'])
        info = ['Source: {}'.format(node['source'])]
        if call_count > 0:
            info.append('Called {} times'.format(node['count']))
            if len(params) > 0:
                info.append('With parameters:')
        return self.info_card(header, info, params)

    def edge_info_card_content(self, edge):
        header = 'Call(s) from {} to {}'.format(edge['caller_name'], edge['called_name'])
        call_count = edge['call_count']
        params = self.view_model.get_params_of_edge(edge['source'], edge['target'])
        info = []
        if call_count > 0:
            info.append('Call made {} times'.format(call_count))
            if len(params) > 0:
                info.append(' With parameters:')
        else:
            info.append('Not traced')
        return self.info_card(header, info, params)

    def dashboard(self):
        return html.Div(
            id='dashboard',
            children=[
                dbc.Tabs(
                    id='tabs',
                    children=[
                        dbc.Tab(label='Realtime', tab_id='realtime-tab', id='realtime-tab', children=[self.tabs.realtime_tab()], tab_style={"margin-left": "auto"}),
                        dbc.Tab(label='Static', tab_id='static-tab', id='static-tab', children=[self.tabs.static_tab()]),
                        dbc.Tab(label='Utilities', tab_id='utilities-tab', id='utilities-tab', children=[self.tabs.utilities_tab()]),
                        dbc.Tab(label='Configure', tab_id='configure-tab', id='configure-tab', children=[self.tabs.configure_tab()]),
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