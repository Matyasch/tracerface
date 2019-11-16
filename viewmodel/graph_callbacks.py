from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from view.info_cards import EdgeInfoCard, NodeInfoCard


def update_graph_value(app, graph, view_model):
    @app.callback(Output('graph-div', 'children'),
        [Input('submit-button', 'n_clicks'),
        Input('timer', 'n_intervals')],
        [State('output-textarea', 'value')])
    def update_graph(out_btn, n_int, output):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'submit-button' and output:
            view_model.output_submit_btn_clicked(output)
        return graph.graph()


def update_graph_style(app, graph, view_model):
    @app.callback(Output('graph', 'stylesheet'),
        [Input('slider', 'value'),
        Input('searchbar', 'value')],
        [State('trace-button', 'on')])
    def update_output(slider, search, trace_on):
        view_model.set_range(slider[0], slider[1])
        return graph.stylesheet(search)


def display_info_card(app, view_model):
    @app.callback(Output('info-card', 'children'),
        [Input('graph', 'tapNodeData'),
        Input('graph', 'tapEdgeData')])
    def update_node_info(node, edge):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[1]
        if id == 'tapNodeData' and node:
            return NodeInfoCard(node, view_model.get_params_of_node(node['id']))
        elif id == 'tapEdgeData' and edge:
            return EdgeInfoCard(edge, view_model.get_params_of_edge(edge['source'], edge['target']))
        raise PreventUpdate