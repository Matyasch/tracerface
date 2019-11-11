from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


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


def display_info_card(app, info_card):
    @app.callback(Output('info-card', 'children'),
        [Input('graph', 'tapNodeData'),
        Input('graph', 'tapEdgeData')])
    def update_node_info(node_data, edge_data):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[1]
        if id == 'tapNodeData' and node_data:
            return info_card.node_card(node_data)
        elif id == 'tapEdgeData' and edge_data:
            return info_card.edge_card(edge_data)
        raise PreventUpdate