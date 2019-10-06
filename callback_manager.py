import json

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

class CallbackManager:
    def __init__(self, app, view_model):
        self.app = app
        self.view_model = view_model

    def setup_callbacks(self):
        self.setup_update_info()
        self.setup_update_elements()
        self.setup_switch_refresher()

    def setup_update_info(self):
        @self.app.callback(Output('info-box', 'children'),
            [Input('output-button', 'n_clicks'),
            Input('refresh-interval', 'n_intervals')])
        def update_info(n_clicks, n_intervals):
            return json.dumps(self.view_model.get_nodes()+[self.view_model.red_count()], indent=2)

    def setup_update_elements(self):
        @self.app.callback(Output('graph', 'elements'),
            [Input('output-button', 'n_clicks'),
            Input('refresh-interval', 'n_intervals')],
            [State('output-textarea', 'value'),
            State('trace-button', 'on')])
        def update_elements(out_btn, n_int, output, trace_on):
            if trace_on:
                return self.view_model.get_nodes() + self.view_model.get_edges()
            elif out_btn and output:
                self.view_model.output_submit_btn_clicked(output)
                return self.view_model.get_nodes() + self.view_model.get_edges()
            else:
                raise PreventUpdate

    def setup_switch_refresher(self):
        @self.app.callback(Output('refresh-interval', 'disabled'),
            [Input('trace-button', 'on')],
            [State('functions', 'value')])
        def switch_refresh_timer(trace_on, functions):
            # TODO: if no functions, don't let turn on
            if trace_on:
                self.view_model.trace_btn_turned_on(functions)
                return False
            else:
                self.view_model.trace_btn_turned_off()
                return True