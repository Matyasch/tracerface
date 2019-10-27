import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_daq as daq
import dash_html_components as html


cyto.load_extra_layouts()


class View:
    def __init__(self, view_model):
        self.view_model = view_model

    def red_selector(self, search):
        return '[count >= {}][id *= "{}"]'.format(self.view_model.red_count(), search)

    def yellow_selector(self, search):
        return '[count >= {}][count < {}][id *= "{}"]'.format(self.view_model.yellow_count(), self.view_model.red_count(), search)

    def green_selector(self, search):
        return '[count > 0][count < {}][id *= "{}"]'.format(self.view_model.yellow_count(), search)

    def graph_stylesheet(self, search=''):
        if not search:
            search = ''
        return [
            {
                'selector': 'node',
                'style': {
                    'content': 'data(id)',
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
            },
            {
                'selector': self.green_selector(search),
                'style': {
                    'border-color': 'green',
                    'color': 'green'
                }
            },
            {
                'selector': self.yellow_selector(search),
                'style': {
                    'border-color': 'orange',
                    'color': 'orange'
                }
            },
            {
                'selector': self.red_selector(search),
                'style': {
                    'border-color': 'red',
                    'color': 'red'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': '#ccc',
                    'label': 'data(params)',
                    'line-color': '#ccc'
                }
            },
        ]

    def graph_layout(self):
        return [cyto.Cytoscape(
            id='graph',
            layout={
                'name': 'dagre',
                'spacingFactor': '3',
            },
            style={
                'width': '100%',
                'height': '95vh'
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
            return dbc.Alert('Configuration saved!', color='success')
        else:
            return dbc.Alert("Couldn't save configuration", color="danger")

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

    def graph_div(self):
        return dbc.Col(
            html.Div(
                id='graph_div',
                children=self.graph_layout()
            )
        )

    def dashboard(self):
        return dbc.Col(
            html.Div(
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
            ),
            width=3
        )

    def realtime_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('List functions to trace'),
                dbc.Input(
                    id='functions',
                    type='text',
                    placeholder='input functions'
                ),
                dbc.FormText('Separated with spcaes')
            ]),
            daq.PowerButton(
                id='trace-button',
                on=False,
                color='#00FF00'
            )
        ])

    def static_tab(self):
        return html.Div(children=[
            'Trace output',
            dbc.Textarea(
                id='output-textarea',
                placeholder='Enter trace output',
                style={'height': '400px'}),
            dbc.Button('Submit',
                id='output-button',
                n_clicks_timestamp=0,
                color='primary',
                className='mr-1')
        ])

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
        ])

    def configure_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('command for bcc: ', width=4),
                dbc.Col(
                    dbc.Input(
                        id='bcc-command',
                        type='text',
                        value='trace-bpfcc',
                        placeholder='command',
                    ),
                    width=8)
                ],
                row=True),
            dbc.Button('Save',
                id='save-config-button',
                n_clicks_timestamp=0,
                color='primary',
                className="mr-1"),
            html.Div(
                id='save-config-notification',
                children=None)
        ])

    def layout(self):
        return html.Div([
            dbc.Row([
                self.graph_div(),
                self.dashboard()
            ]),
            dcc.Interval(
                id='timer',
                interval=1*500, # in milliseconds
                n_intervals=0,
                disabled=True
            )
        ])