'''
This module contains all callbacks regarding
the configuration setting in the configure tab
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import view.alerts as alerts
from view.graph import Graph


# Save animation status and spacing between nodes
def save_graph_layout_config(app, view_model):
    @app.callback(Output('graph', 'layout'),
        [Input('save-config-button', 'n_clicks')],
        [State('animate-switch', 'value'),
        State('node-spacing-input', 'value')])
    def update_layout(save_btn, animate_switch, spacing):
        if save_btn:
            animate = len(animate_switch) == 1
            view_model.save_layout_config(animate, spacing)
        return Graph.layout(spacing=view_model.get_spacing_config(), animate=view_model.get_animate_config())
