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


def graph_layout(view_model):
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
            elements= view_model.get_nodes() + view_model.get_edges(),
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
                    'selector': '[count > {}]'.format(view_model.green_count()),
                    'style': {
                        'border-color': 'green',
                        'color': 'green'
                    }
                },
                {
                    'selector': '[count > {}]'.format(view_model.yellow_count()),
                    'style': {
                        'border-color': 'orange',
                        'color': 'orange'
                    }
                },
                {
                    'selector': '[count > {}]'.format(view_model.red_count()),
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


def dashboard():
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
            ])
        ]
    )