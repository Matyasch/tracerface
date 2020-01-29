'''
This module contains all callbacks regarding
the shown graph including the information cards
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from view.info_cards import EdgeInfoCard, NodeInfoCard
from view.graph import Graph


# Update nodes and edges in graph
def update_graph_elements(app, view_model):
    @app.callback(Output('graph', 'elements'),
        [Input('submit-button', 'n_clicks'),
        Input('timer', 'n_intervals')],
        [State('output-textarea', 'value')])
    def update_elements(out_btn, n_int, output):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'submit-button' and output:
            view_model.output_submit_btn_clicked(output)
        return view_model.get_nodes() + view_model.get_edges()


# Update colors of the graph
def update_graph_style(app, view_model):
    @app.callback(Output('graph', 'stylesheet'),
        [Input('slider', 'value'),
        Input('searchbar', 'value'),
        Input('graph', 'elements')])
    def update_style(slider, search, elements):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'slider':
            view_model.set_range(slider[0], slider[1])
        return Graph.stylesheet(search, view_model.yellow_count(), view_model.red_count())


# Display info card for clicked element in graph
def display_info_card(app, view_model):
    @app.callback(Output('info-card', 'children'),
        [Input('graph', 'tapNodeData'),
        Input('graph', 'tapEdgeData'),
        Input('graph', 'elements')])
    def update_node_info(node, edge, elements):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[1]
        if id == 'tapNodeData' and node:
            return NodeInfoCard(node, view_model.get_params_of_node(node['id']))
        elif id == 'tapEdgeData' and edge:
            return EdgeInfoCard(edge, view_model.get_params_of_edge(edge['source'], edge['target']))
        elif id == 'elements' and elements:
            return None
        raise PreventUpdate
