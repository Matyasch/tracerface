import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

cyto.load_extra_layouts()


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


class View:
    def __init__(self, view_model):
        self.view_model = view_model

    def graph_layout(self):
        return html.Div(
        className='large column',
        children=[
            cyto.Cytoscape(
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
                stylesheet=[
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
                        'selector': '[count > {}]'.format(self.view_model.green_count()),
                        'style': {
                            'border-color': 'green',
                            'color': 'green'
                        }
                    },
                    {
                        'selector': '[count > {}]'.format(self.view_model.yellow_count()),
                        'style': {
                            'border-color': 'orange',
                            'color': 'orange'
                        }
                    },
                    {
                        'selector': '[count > {}]'.format(self.view_model.red_count()),
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
            )
        ]
    )

    def dashboard(self):
        return html.Div(
            className='small column',
            children=[
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
                    id='interval-component',
                    interval=1*500, # in milliseconds
                    n_intervals=0
                ),
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Tab one', value='tab-1'),
                    dcc.Tab(label='Tab two', value='tab-2'),
                ]),
                html.Div(id='tabs-content')
            ]
        )

    def app_layout(self):
        return html.Div([
            self.graph_layout(),
            self.dashboard()
        ])