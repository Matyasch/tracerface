'''
This module contains all callbacks regarding
the shown graph including the information cards
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from tracerface.load_output import load_trace_output_from_file_to_call_graph
from tracerface.web_ui.alerts import ErrorAlert
from tracerface.web_ui.graph import Graph
from tracerface.web_ui.styles import expanded_style
from tracerface.web_ui.ui_format import (
    convert_edges_to_cytoscape_format,
    convert_nodes_to_cytoscape_format
)


# Update nodes and edges in graph
def update_graph_elements(app, call_graph):
    output = [
        Output('graph', 'elements'),
        Output('load-output-notification', 'children')
    ]
    input = [
        Input('load-output-button', 'n_clicks'),
        Input('timer', 'n_intervals')
    ]
    state = [State('output-path', 'value')]
    @app.callback(output, input, state)
    def update_elements(load, timer, file_path):
        if not callback_context.triggered:
            raise PreventUpdate

        alert = None
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'load-output-button' and file_path:
            try:
                load_trace_output_from_file_to_call_graph(file_path, call_graph)
            except FileNotFoundError:
                alert = ErrorAlert('Could not find output file at {}'.format(file_path))
            except IsADirectoryError:
                alert = ErrorAlert('{} is a directory, not a file'.format(file_path))
        elif id == 'load-output-button' :
            alert = ErrorAlert('No path given')

        edges = convert_edges_to_cytoscape_format(call_graph.get_nodes(), call_graph.get_edges())
        nodes = convert_nodes_to_cytoscape_format(call_graph.get_nodes(), call_graph.get_edges())
        return nodes + edges, alert


# Display or hide inforamtion about edges and nodes
# Update colors of the graph
def update_graph_style(app, call_graph):
    output = Output('graph', 'stylesheet')
    input = [
        Input('slider', 'value'),
        Input('searchbar', 'value'),
        Input('graph', 'elements'),
        Input('graph', 'tapNodeData'),
        Input('graph', 'tapEdgeData')
    ]
    @app.callback(output, input)
    def update_style(slider, search, elements, node, edge):
        if not callback_context.triggered:
            raise PreventUpdate

        input = callback_context.triggered[0]['prop_id'].split('.')
        if input[0] == 'slider':
            call_graph.set_colors(slider[0], slider[1])
        if input[0] == 'graph' and input[1] == 'tapNodeData' and node:
            call_graph.element_clicked(node['id'])
        if input[0] == 'graph' and input[1] == 'tapEdgeData' and edge:
            call_graph.element_clicked(edge['id'])

        if not search:
            search = ''
        base_styles = Graph.stylesheet(search, call_graph.get_yellow(), call_graph.get_red())
        node_styles = [expanded_style(id) for id in call_graph.get_expanded_elements()]
        return base_styles + node_styles
