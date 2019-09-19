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
                'animate': True,
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
                        'shape': 'rectangle',
                        'border-color': 'black',
                        'background-color': 'white',
                        'border-width': '1',
                        'width': 'label'
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
                    children=f'Layout',
                    style={'margin-left': '3px'}
                ),
                dcc.Dropdown(
                    id='dropdown-layout',
                    value='dagre',
                    clearable=False,
                    options=[
                        {'label': name.capitalize(), 'value': name}
                        for name in ['dagre', 'klay', 'breadthfirst']
                    ],
                )
            ]),
            html.P(
                children=f'Info',
                style={'margin-left': '3px'}
            ),
            html.Pre(
                id='cytoscape-tapNodeData-json',
                style=styles['pre']
            )
        ]
    )


def dashboard_infopanel():
    pass