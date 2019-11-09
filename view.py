import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_daq as daq
import dash_html_components as html

from utils import c_type_pairs

cyto.load_extra_layouts()


class View:
    def __init__(self, view_model):
        self.view_model = view_model

    def base_node_style(self):
        return {
                'selector': 'node',
                'style': {
                    'content': 'data(name)',
                    'text-valign': 'center',
                    'width': 'label',
                    'height': 'label',
                    'shape': 'rectangle',
                    'border-color': 'grey',
                    'color': 'grey',
                    'background-color': 'white',
                    'border-width': '1',
                    'padding': '5px'
                }
            }

    def green_node_style(self, search):
        return {
                'selector': '[count > 0][count < {}][name *= "{}"]'.format(self.view_model.yellow_count(), search),
                'style': {
                    'border-color': 'green',
                    'color': 'green'
                }
            }

    def yellow_node_style(self, search):
        return {
                'selector': '[count >= {}][count < {}][name *= "{}"]'.format(self.view_model.yellow_count(), self.view_model.red_count(), search),
                'style': {
                    'border-color': 'orange',
                    'color': 'orange'
                }
            }

    def red_node_style(self, search):
        return {
                'selector': '[count >= {}][name *= "{}"]'.format(self.view_model.red_count(), search),
                'style': {
                    'border-color': 'red',
                    'color': 'red'
                }
            }

    def base_edge_style(self):
        return {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': '#ccc',
                    'label': 'data(params)',
                    'line-color': '#ccc'
                }
            }

    def green_edge_style(self, search):
        return {
                'selector': '[call_count > 0][call_count < {}][called_name *= "{}"]'.format(self.view_model.yellow_count(), search),
                'style': {
                    'line-color': 'green',
                    'target-arrow-color': 'green',
                    'width': '1'
                }
            }

    def yellow_edge_style(self, search):
        return {
                'selector': '[call_count >= {}][call_count < {}][called_name *= "{}"]'.format(self.view_model.yellow_count(), self.view_model.red_count(), search),
                'style': {
                    'line-color': 'orange',
                    'target-arrow-color': 'orange',
                    'width': '1'
                }
            }

    def red_edge_style(self, search):
        return {
                'selector': '[call_count >= {}][called_name *= "{}"]'.format(self.view_model.red_count(), search),
                'style': {
                    'line-color': 'red',
                    'target-arrow-color': 'red',
                    'width': '1'
                }
            }

    def graph_stylesheet(self, search=''):
        if not search:
            search=''
        return [self.base_node_style(),
                self.green_node_style(search),
                self.yellow_node_style(search),
                self.red_node_style(search),
                self.base_edge_style(),
                self.green_edge_style(search),
                self.yellow_edge_style(search),
                self.red_edge_style(search)
        ]

    def button_style(self):
        return {'margin-top': '10px'}

    def tab_style(self):
        return {'padding': '0px 20px 0px 20px'}

    def graph_layout(self):
        return [cyto.Cytoscape(
            id='graph',
            layout={
                'name': 'dagre',
                'spacingFactor': '3',
                'animate': self.view_model.animate_config()
            },
            style={
                'height': '100vh'
            },
            elements= self.view_model.get_nodes() + self.view_model.get_edges(),
            stylesheet=self.graph_stylesheet()
        )]

    def search_div(self):
        return dbc.Input(
            id='searchbar',
            type='text',
            placeholder='function name')

    def save_config_alert(self, success):
        if success:
            message = 'Configuration saved!'
            color = 'success'
        else:
            message = 'Could not save configuration!'
            color = 'danger'
        return dbc.Alert(message, color=color, duration=4000, dismissable=True)

    def load_output_alert(self, success):
        if success:
            message = 'Output successfully loaded'
            color = 'success'
        else:
            message = 'There was an error loading this output!'
            color = 'danger'
        return dbc.Alert(message, color=color, duration=4000, dismissable=True)

    def add_app_alert(self, success, app=''):
        if success:
            message = '{} was added successfully'.format(app)
            color = 'success'
        else:
            message = 'There was an error adding the path!'
            color = 'danger'
        return dbc.Alert(message, color=color, duration=4000, dismissable=True)

    def slider_div(self, disabled=False):
        return [
            dcc.RangeSlider(
                id='slider',
                min=1,
                max=self.view_model.max_count(),
                value=[round(self.view_model.model.yellow_count()), round(self.view_model.model.red_count())],
                pushable=1,
                disabled=disabled,
                marks={
                    1: {'label': '1', 'style': {'color': 'green'}},
                    self.view_model.max_count(): {'label': '{}'.format(self.view_model.max_count()), 'style': {'color': 'red'}}
                },
                tooltip = { 'always_visible': not disabled }
            )
        ]

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

    def graph_div(self):
        return html.Div(
                id='graph_div',
                children=self.graph_layout()
            )

    def dashboard(self):
        return html.Div(
            id='dashboard',
            children=[
                dbc.Tabs(
                    id='tabs',
                    children=[
                        dbc.Tab(label='Realtime', tab_id='realtime-tab', id='realtime-tab', children=[self.realtime_tab()], tab_style={"margin-left": "auto"}),
                        dbc.Tab(label='Static', tab_id='static-tab', id='static-tab', children=[self.static_tab()]),
                        dbc.Tab(label='Utilities', tab_id='utilities-tab', id='utilities-tab', children=[self.utilities_tab()]),
                        dbc.Tab(label='Configure', tab_id='configure-tab', id='configure-tab', children=[self.configure_tab()]),
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

    def manage_application_dialog(self, app='', options=[]):
        return [
            dbc.ModalHeader('Manage functions of {}'.format(app)),
            dbc.ModalBody([
                dbc.FormGroup([
                    dbc.Label('Add function to trace'),
                    dbc.Row([
                        dbc.Col(dbc.Input(
                            id='function-name',
                            type='text',
                            placeholder='function name'
                        )),
                        dbc.Col(
                            dbc.Button('Add',
                                id='add-func-button',
                                color='primary',
                                className='mr-1'),
                            width=2)]),
                    dbc.FormText('Write name of the function and click add')]),
                dbc.FormGroup([
                    dbc.Label('Manage functions'),
                    dbc.Select(
                        id='functions-select',
                        options=[{"label": name, "value": name} for name in options]),
                    dbc.Button('Manage parameters',
                        id='add-params-button',
                        color='success',
                        className='mr-1',
                        style=self.button_style()),
                    dbc.Button('Remove function',
                        id='remove-func-button',
                        color='danger',
                        className='mr-1',
                        style=self.button_style())])
            ]),
            dbc.ModalFooter(
                dbc.Button('Close', id='close-app-dialog', className='ml-auto'))]

    def manage_function_dialog(self, func='', options=[]):
        return [
            dbc.ModalHeader('Manage parameters of {}'.format(func)),
            dbc.ModalBody([
                dbc.FormGroup([
                    dbc.Label('Add parameter to trace'),
                    dbc.Row([
                        dbc.Col(dbc.Select(
                                id='param-type',
                                options=[{"label": c_type[0], "value": '{}:{}'.format(c_type[0], c_type[1])} for c_type in c_type_pairs()])),
                        dbc.Col(dbc.Input(
                                id='param-index',
                                type='number',
                                min=1)),
                        dbc.Col(
                            dbc.Button('Add',
                                id='add-param-button',
                                color='primary',
                                className='mr-1'),
                            width=2)]),
                    dbc.FormText('Write the name of the parameter as it is in the code')]),
                dbc.FormGroup([
                    dbc.Label('Manage parameters'),
                    dbc.Select(
                        id='params-select',
                        options=[{"label": name, "value": name} for name in options]),
                    dbc.Button('Remove parameter',
                        id='remove-param-button',
                        color='danger',
                        className='mr-1',
                        style=self.button_style())])
            ]),
            dbc.ModalFooter(
                dbc.Button('Close', id='close-func-dialog', className='ml-auto'))]

    def realtime_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Add application to trace'),
                dbc.Row([
                    dbc.Col(dbc.Input(
                        id='application-path',
                        type='text',
                        placeholder='/path/to/binary'
                    )),
                    dbc.Col(dbc.Button('Add',
                        id='add-app-button',
                        color='primary',
                        className='mr-1'),
                    width=2)
                ]),
                dbc.FormText('Write path to runnable and click add'),
                html.Div(
                    id='add-app-notification',
                    children=None,
                    style=self.button_style())
            ]),
            dbc.FormGroup([
                dbc.Label('Manage applications'),
                dbc.Select(
                    id='applications-select',
                    options=[]),
                dbc.Button('Manage functions',
                    id='add-function-button',
                    color='success',
                    className='mr-1',
                    style=self.button_style()),
                dbc.Button('Remove application',
                    id='remove-app-button',
                    color='danger',
                    className='mr-1',
                    style=self.button_style())
                ]),
            dbc.Checklist(
                options=[
                    {"label": "Use config file instead", "value": 'config'}
                ],
                value=[],
                id="use-config-file-switch",
                switch=True,
            ),
            dbc.Collapse(
                dbc.Input(
                    id='config-file-path',
                    type='text',
                    placeholder='/path/to/config'
                ),
                id="config-fine-input-collapse",
            ),
            daq.PowerButton(
                id='trace-button',
                on=False,
                color='#00FF00'),
            dbc.Modal(children=self.manage_application_dialog(),
                id='app-dialog',
                scrollable=True),
            dbc.Modal(children=self.manage_function_dialog(),
                id='func-dialog',
                scrollable=True)
        ],
        style=self.tab_style())

    def static_tab(self):
        return html.Div([
            dbc.FormGroup([
                dbc.Label('Trace output'),
                dbc.Textarea(
                    id='output-textarea',
                    placeholder='Enter trace output',
                    style={'height': '200px'}),
                dbc.Button('Submit',
                    id='submit-button',
                    color='primary',
                    className='mr-1',
                    style=self.button_style()),
                html.Div(
                    id='load-output-notification',
                    children=None,
                    style=self.button_style())
            ])
        ],
        style=self.tab_style())

    def utilities_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Update coloring'),
                html.Div(
                    id='slider-div',
                    children=self.slider_div(),
                    style={'padding': '40px 0px 20px 0px'}
                )]),
            dbc.FormGroup([
                dbc.Label('Search function', width=4),
                dbc.Col(
                    html.Div(
                        id='search-div',
                        children=[self.search_div()]),
                    width=8)
            ],
            row=True)
        ],
        style=self.tab_style())

    def configure_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('command for bcc: ', width=5),
                dbc.Col(
                    dbc.Input(
                        id='bcc-command',
                        type='text',
                        value='trace-bpfcc',
                        placeholder='command',
                    ))
                ],
                row=True),
            dbc.Checklist(
                options=[
                    {"label": "Animate graph", "value": 'animate'}
                ],
                value=[],
                id="animate-switch",
                switch=True,
            ),
            dbc.Button('Save',
                id='save-config-button',
                color='primary',
                className="mr-1"),
            html.Div(
                id='save-config-notification',
                children=None,
                style=self.button_style())
        ],
        style=self.tab_style())

    def layout(self):
        return html.Div([
            dbc.Row([
                dbc.Col(self.graph_div(), width=9),
                dbc.Col(self.dashboard())
            ],
            style={'width': '100%'}),
            dcc.Interval(
                id='timer',
                interval=1*500, # in milliseconds
                n_intervals=0,
                disabled=True
            )
        ])