import dash_bootstrap_components as dbc
from dash_html_components import P

class InfoCard:
    def __init__(self, view_model):
        self.view_model = view_model

    def info_card(self, header, infos, params):
        return dbc.Card([
            dbc.CardHeader(header),
            dbc.CardBody([P(info) for info in infos] + [
                dbc.ListGroup(
                    [dbc.ListGroupItem(', '.join(param)) for param in params],
                    className='scrollable',
                    style={'max-height': '200px'})
            ])],
            color='light',
            style={'margin': '20px'})

    def node_card(self, node):
        header = node['name']
        call_count = node['count']
        params = self.view_model.get_params_of_node(node['id'])
        info = ['Source: {}'.format(node['source'])]
        if call_count > 0:
            info.append('Called {} times'.format(node['count']))
            if len(params) > 0:
                info.append('With parameters:')
        return self.info_card(header, info, params)

    def edge_card(self, edge):
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