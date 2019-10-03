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
        self.setup_turn_off_refresher()

    def setup_update_info(self):
        @self.app.callback(Output('info-box', 'children'),
            [Input('output-button', 'n_clicks')],
            [State('output-textarea', 'value')])
        def update_info(n, value):
            if not n:
                raise PreventUpdate
            return json.dumps(self.view_model.get_nodes()+[self.view_model.red_count()], indent=2)

    def setup_update_elements(self):
        @self.app.callback(Output('graph', 'elements'),
            [Input('output-button', 'n_clicks'),
            Input('refresh-interval', 'n_intervals')],
            [State('output-textarea', 'value')])
        def update_elements(n_click, n_int, value):
            if not n_click:
                raise PreventUpdate
            elif value:
                self.view_model.output_submit_button_clicked(value)
            return self.view_model.get_nodes() + self.view_model.get_edges()

    def setup_turn_off_refresher(self):
        @self.app.callback(Output('refresh-interval', 'disabled'),
            [Input('output-button', 'n_clicks')])
        def turn_off_refresh_timer(n_click):
            if not n_click:
                raise PreventUpdate
            else:
                return True