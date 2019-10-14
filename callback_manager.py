import json

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

class CallbackManager:
    def __init__(self, app, view_model, layout):
        self.app = app
        self.view_model = view_model
        self.layout = layout

    def setup_callbacks(self):
        self.setup_update_info()
        self.setup_update_graph()
        self.setup_switch_refresher()
        self.setup_slider_button_event()
        self.setup_update_colors()

    def setup_update_info(self):
        @self.app.callback(Output('info-box', 'children'),
            [Input('output-button', 'n_clicks'),
            Input('refresh-interval', 'n_intervals'),
            Input('slider', 'value')])
        def update_info(n_clicks, n_intervals, value):
            return self.layout.yellow_selector() + ' {} - {} - {}'.format(value[0], value[1], self.view_model.model.persistence.red)

    def setup_update_graph(self):
        @self.app.callback(Output('graph_div', 'children'),
            [Input('output-button', 'n_clicks'),
            Input('refresh-interval', 'n_intervals')],
            [State('output-textarea', 'value'),
            State('trace-button', 'on')])
        def update_graph(out_btn, n_int, output, trace_on):
            if not trace_on and not out_btn:
                raise PreventUpdate
            elif not trace_on and out_btn and out_btn:
                self.view_model.output_submit_btn_clicked(output)
            return self.layout.graph_layout()

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

    def setup_slider_button_event(self):
        @self.app.callback(Output('slider-tab', 'children'),
            [Input('slider-button', 'n_clicks')],
            [State('trace-button', 'on')])
        def activate_slider(btn, trace_on):
            if trace_on:
                raise PreventUpdate
            elif btn:
                return self.layout.slider()

    def setup_update_colors(self):
        @self.app.callback(Output('graph', 'stylesheet'),
            [Input('slider', 'value')],
            [State('trace-button', 'on')])
        def update_output(value, trace_on):
            if trace_on:
                raise PreventUpdate
            self.view_model.set_range(value[0], value[1])
            return self.layout.graph_stylesheet()