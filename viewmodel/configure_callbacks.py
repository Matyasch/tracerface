from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import view.alerts as alerts


def save_graph_layout_config(app, graph, view_model):
    @app.callback(Output('graph', 'layout'),
        [Input('save-config-button', 'n_clicks')],
        [State('animate-switch', 'value'),
        State('node-spacing-input', 'value')])
    def update_layout(save_btn, animate_switch, spacing):
        if save_btn:
            animate = len(animate_switch) == 1
            view_model.save_layout_config(animate, spacing)
        return graph.layout()


def save_bcc_command_config(app, view_model):
    @app.callback(Output('save-config-notification', 'children'),
        [Input('save-config-button', 'n_clicks')],
        [State('bcc-command', 'value')])
    def save_clicked(save_btn, bcc_command):
        if save_btn:
            if bcc_command:
                view_model.save_app_config(bcc_command)
                return alerts.save_config_success_alert()
            else:
                return alerts.empty_command_config_alert()
        raise PreventUpdate