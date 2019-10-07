import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

import dash_cytoscape as cyto

cyto.load_extra_layouts()


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


class Layout:
    def __init__(self, view_model):
        self.view_model = view_model

    def graph_stylesheet(self):
        [
            {
                'selector': 'node',
                'style': {
                    'content': 'data(id)',
                    'text-valign': 'center',
                    'width': 'label',
                    'height': 'label',
                    'shape': 'rectangle',
                    'border-color': 'black',
                    'background-color': 'white',
                    'border-width': '1',
                    'padding': '5px'
                }
            },
            {
                'selector': '[count = 0]',
                'style': {
                    'border-color': 'grey',
                    'color': 'grey'
                }
            },
            {
                'selector': self.view_model.green_selector(),
                'style': {
                    'border-color': 'green',
                    'color': 'green'
                }
            },
            {
                'selector': self.view_model.yellow_selector(),
                'style': {
                    'border-color': 'orange',
                    'color': 'orange'
                }
            },
            {
                'selector': self.view_model.red_selector(),
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

    def render_graph_layout(self):
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

    def graph_layout(self):
        return html.Div(
        className='large column',
        id='graph_layout',
        children=self.render_graph_layout()
        )

    def dashboard(self):
        return html.Div(
            className='small column',
            children=[
                dcc.Tabs(id='mode-tabs', value='realtime-tab', children=[
                    dcc.Tab(label='Realtime mode', value='realtime-tab', children=[self.realtime_tab()]),
                    dcc.Tab(label='Static mode', value='static-tab',children=[self.output_tab()]),
                ]),
                html.Div(id='tabs-content'),
                dcc.Tab(children=[
                    html.P(
                        children=f'Info',
                        style={'margin-left': '3px'}
                    ),
                    html.Pre(
                        id='info-box',
                        style=styles['pre']
                    )
                ]),
                dcc.Interval(
                    id='refresh-interval',
                    interval=1*500, # in milliseconds
                    n_intervals=0,
                    disabled=True
                )
            ]
        )

    def app_layout(self):
        return html.Div([
            self.graph_layout(),
            self.dashboard()
        ])

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

    def output_tab(self):
        return html.Div(children=[
            html.P('Trace output'),
            dcc.Textarea(
                id='output-textarea',
                placeholder='Enter trace output',
                style={'width': '100%', 'height': '600px'},
            ),
            html.Button('Submit', id='output-button', n_clicks_timestamp=0)
        ])