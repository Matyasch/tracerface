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

    def graph_div(self):
        return html.Div(
            className='large column',
            id='graph_div',
            children=self.graph_layout()
        )

    def search_div(self):
        return [
            'Search node: ',
            dcc.Input(
                id='searchbar',
                type='text',
                placeholder='function name'
            )
        ]

    def slider_div(self, disabled=False):
        return [
            'Update coloring',
            dcc.RangeSlider(
                id='slider',
                min=1,
                max=self.view_model.max_count(),
                value=[round(self.view_model.model.yellow_count()), round(self.view_model.model.red_count())],
                pushable=1,
                disabled=disabled
            )
        ]

    def dashboard(self):
        return html.Div(
            className='small column',
            id='dashboard',
            children=[
                dcc.Tabs(
                    id='mode-tabs',
                    children=[
                        dcc.Tab(label='Realtime', value='realtime-tab', id='realtime-tab', children=[self.realtime_tab()]),
                        dcc.Tab(label='Static', value='static-tab', id='static-tab', children=[self.static_tab()]),
                        dcc.Tab(label='Utilities', value='utilities-tab', id='utilities-tab', children=[self.utilities_tab()]),
                        dcc.Tab(label='Configure', value='configure-tab', id='configure-tab', children=[self.configure_tab()]),
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
        )

    def realtime_tab(self):
        return html.Div(children=[
            html.P('List functions to trace'),
            html.P('Separated with spcaes'),
            dcc.Input(
                id='functions',
                type='text',
                placeholder='input functions',
                style={'width': '97%'}
            ),
            daq.PowerButton(
                id='trace-button',
                on=False,
                color='#00FF00'
            )
        ])

    def static_tab(self):
        return html.Div(children=[
            'Trace output',
            dcc.Textarea(
                id='output-textarea',
                placeholder='Enter trace output',
                style={'width': '100%', 'height': '400px'},
            ),
            html.Button('Submit', id='output-button', n_clicks_timestamp=0)
        ])

    def utilities_tab(self):
        return html.Div(children=[
            html.Div(
                id='slider-div',
                children=self.slider_div()
            ),
            html.Div(
                id='search-div',
                children=self.search_div()
            )
        ])

    def configure_tab(self):
        return html.Div(children=[
            html.Div(
                children=[
                    'command for bcc: ',
                    dcc.Input(
                        id='bcc-command',
                        type='text',
                        value='trace-bpfcc',
                        placeholder='command',
                    )
                ]
            ),
            html.Div(children=[
                html.Button('Save', id='save-config-button', n_clicks_timestamp=0),
                html.Div(id='save-config-notification', children='')
                ])
        ])

    def layout(self):
        return html.Div([
            self.graph_div(),
            self.dashboard(),
            dcc.Interval(
                id='timer',
                interval=1*500, # in milliseconds
                n_intervals=0,
                disabled=True
            )
        ])