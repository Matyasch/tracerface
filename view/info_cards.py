import dash_bootstrap_components as dbc
from dash_html_components import P


# Parent class of the two types of info-cards
class BaseInfoCard(dbc.Card):
    def __init__(self, header, info, params):
        super().__init__(children=self._content(header, info, params), color='light', style={'margin': '20px'})

    def _content(self, header, infos, params):
        return [
            dbc.CardHeader(header),
            dbc.CardBody([P(info) for info in infos] + [
                dbc.ListGroup(
                    [dbc.ListGroupItem(', '.join(param)) for param in params],
                    className='scrollable',
                    style={'max-height': '200px'})])]


# Info card for nodes/functions
class NodeInfoCard(BaseInfoCard):
    def __init__(self, node, params):
        header = node['name']
        call_count = node['count']
        info = ['Source: {}'.format(node['source'])]
        if call_count > 0:
            info.append('Called {} times'.format(node['count']))
            if len(params) > 0:
                info.append('With parameters:')
        super().__init__(header, info, params)


# Info card for edges/calls
class EdgeInfoCard(BaseInfoCard):
    def __init__(self, edge, params):
        header = 'Call(s) from {} to {}'.format(edge['caller_name'], edge['called_name'])
        call_count = edge['call_count']
        info = []
        if call_count > 0:
            info.append('Call made {} times'.format(call_count))
            if len(params) > 0:
                info.append(' With parameters:')
        else:
            info.append('Not traced')
        super().__init__(header, info, params)
