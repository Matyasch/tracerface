'''
This module contains all callbacks regarding
the shown graph including the information cards
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from view.alerts import ErrorAlert
from view.graph import Graph
from view.styles import expanded_style


# Update nodes and edges in graph
def update_graph_elements(app, view_model):
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
    def update_elements(load, time, output_path):
        if not callback_context.triggered:
            raise PreventUpdate

        alert = None
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'load-output-button':
            try:
                view_model.load_output(output_path)
            except ValueError as msg:
                alert = ErrorAlert(str(msg))
        return view_model.get_nodes() + view_model.get_edges(), alert


# Display or hide inforamtion about edges and nodes
# Update colors of the graph
def update_graph_style(app, view_model):
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
            view_model.set_range(slider[0], slider[1])
        if input[0] == 'graph' and input[1] == 'tapNodeData' and node:
            view_model.element_clicked(node['id'])
        if input[0] == 'graph' and input[1] == 'tapEdgeData' and edge:
            view_model.element_clicked(edge['id'])

        base_styles = Graph.stylesheet(search, view_model.yellow_count(), view_model.red_count())
        node_styles = [expanded_style(id) for id in view_model.get_expanded_elements()]
        return base_styles + node_styles
