import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_daq as daq
import dash_html_components as html

from view.dialogs import manage_application_dialog, manage_function_dialog
import view.styles as styles


cyto.load_extra_layouts()


class View:
    def __init__(self, view_model):
        self.view_model = view_model

    def graph_stylesheet(self, search=''):
        if not search:
            search=''
        return [
            styles.base_node_style(),
            styles.green_node_style(self.view_model.yellow_count(), search),
            styles.yellow_node_style(self.view_model.yellow_count(), self.view_model.red_count(), search),
            styles.red_node_style(self.view_model.red_count(), search),
            styles.base_edge_style(),
            styles.green_edge_style(self.view_model.yellow_count(), search),
            styles.yellow_edge_style(self.view_model.yellow_count(), self.view_model.red_count(), search),
            styles.red_edge_style(self.view_model.red_count(), search)
        ]

    def graph_layout(self):
        return {
            'name': 'dagre',
            'spacingFactor': self.view_model.spacing_config(),
            'animate': self.view_model.animate_config()
        }

    def graph(self):
        return [cyto.Cytoscape(
            id='graph',
            layout=self.graph_layout(),
            style={'height': '100vh'},
            elements= self.view_model.get_nodes() + self.view_model.get_edges(),
            stylesheet=self.graph_stylesheet()
        )]

    def search_div(self):
        return [dbc.Input(
            id='searchbar',
            type='text',
            placeholder='function name',
            disabled=self.view_model.max_count() < 1)]

    def slider_div(self):
        disabled = self.view_model.max_count() < 1
        return [dcc.RangeSlider(
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
                    tooltip = { 'always_visible': not disabled })]

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
                id='graph-div',
                children=self.graph()
            )

    def config_path_swtich(self, disabled=False):
        return [{"label": "Use config file instead", "value": 'config', 'disabled': disabled}]

    def config_path_div(self):
        return [
            dbc.Checklist(
                options=self.config_path_swtich(),
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
            )
        ]

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
                    style=styles.button_style())
            ]),
            dbc.FormGroup([
                dbc.Label('Manage applications'),
                dbc.Select(
                    id='applications-select',
                    options=[]),
                dbc.Button('Manage functions',
                    id='manage-functions-button',
                    color='success',
                    className='mr-1',
                    style=styles.button_style()),
                dbc.Button('Remove application',
                    id='remove-app-button',
                    color='danger',
                    className='mr-1',
                    style=styles.button_style()),
                html.Div(
                    id='manage-apps-notification',
                    children=None,
                    style=styles.button_style())
                ]),
            html.Div(
                id='config-path-div',
                children=self.config_path_div(),
                style=styles.button_style()),
            daq.PowerButton(
                id='trace-button',
                on=False,
                color='#00FF00'),
            html.Div(
                id='trace-error-notification',
                children=None,
                style=styles.button_style()),
            dbc.Modal(children=manage_application_dialog(),
                id='app-dialog',
                scrollable=True),
            dbc.Modal(children=manage_function_dialog(),
                id='func-dialog',
                scrollable=True)
        ],
        style=styles.tab_style())

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
                    style=styles.button_style()),
                html.Div(
                    id='load-output-notification',
                    children=None,
                    style=styles.button_style())
            ])
        ],
        style=styles.tab_style())

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
                        children=self.search_div()),
                    width=8)
            ],
            row=True)
        ],
        style=styles.tab_style())

    def configure_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Command for bcc: ', width=5),
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
                value=['animate'],
                id="animate-switch",
                switch=True),
            dbc.FormGroup([
                dbc.Label('Spacing between nodes: ', width=7),
                dbc.Col(
                    dbc.Input(
                        id='node-spacing-input',
                        type='number',
                        min=1,
                        value=2))
                ],
                row=True),
            dbc.Button('Save',
                id='save-config-button',
                color='primary',
                className="mr-1"),
            html.Div(
                id='save-config-notification',
                children=None,
                style=styles.button_style())
        ],
        style=styles.tab_style())

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