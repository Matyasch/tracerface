import json

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

class CallbackManager:
    def __init__(self, app, view_model, layout):
        self.app = app
        self.view_model = view_model
        self.layout = layout

    def setup_callbacks(self):
        self.info_box_value_callback()
        self.graph_value_callback()
        self.timer_disabled_callback()
        self.slider_visibility_callback()
        self.graph_stylesheet_callback()
        self.config_save_notification_callback()
        self.static_tab_disabled_callback()
        self.utilities_tab_disabled_callback()
        self.searchbar_disabled_callback()

    def info_box_value_callback(self):
        @self.app.callback(Output('info-box', 'children'),
            [Input('output-button', 'n_clicks'),
            Input('timer', 'n_intervals'),
            Input('slider', 'value')])
        def update_info(n_clicks, n_intervals, value):
            return self.layout.yellow_selector('') + ' {} - {} - {}'.format(value[0], value[1], self.view_model.model._persistence.red)

    def graph_value_callback(self):
        @self.app.callback(Output('graph_div', 'children'),
            [Input('output-button', 'n_clicks'),
            Input('timer', 'n_intervals')],
            [State('output-textarea', 'value')])
        def update_graph(out_btn, n_int, output):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'output-button' and output:
                self.view_model.output_submit_btn_clicked(output)
            return self.layout.graph_layout()

    def timer_disabled_callback(self):
        @self.app.callback(Output('timer', 'disabled'),
            [Input('trace-button', 'on')],
            [State('functions', 'value'),
            State('timer', 'disabled')])
        def switch_timer_state(trace_on, functions, disabled):
            # TODO: if no functions, don't let turn on
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            if trace_on:
                self.view_model.trace_btn_turned_on(functions)
            elif not disabled:
                self.view_model.trace_btn_turned_off()
            return not trace_on

    def slider_visibility_callback(self):
        @self.app.callback(Output('slider-div', 'children'),
            [Input('mode-tabs', 'value')])
        def show_slider(tab):
            disabled = not self.view_model.max_count() > 0
            if tab == 'utilities-tab':
                return self.layout.slider_div(disabled)
            return None

    def static_tab_disabled_callback(self):
        @self.app.callback(Output('static-tab', 'disabled'),
            [Input('trace-button', 'on')])
        def disable_static_tab(trace_on):
            return trace_on

    def searchbar_disabled_callback(self):
        @self.app.callback(Output('searchbar', 'disabled'),
            [Input('mode-tabs', 'value')])
        def disable_searchbar(tab):
            return tab == 'utilities-tab' and not self.view_model.max_count() > 0

    def utilities_tab_disabled_callback(self):
        @self.app.callback(Output('utilities-tab', 'disabled'),
            [Input('trace-button', 'on')])
        def disable_utilities_tab(trace_on):
            return trace_on

    def config_save_notification_callback(self):
        @self.app.callback(Output('save-config-notification', 'children'),
            [Input('save-config-button', 'n_clicks'),
            Input('mode-tabs', 'value')],
            [State('bcc-command', 'value')])
        def save_clicked(save_btn, tab, bcc_command):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'save-config-button':
                self.view_model.save_config(bcc_command)
                return 'Saved'
            else:
                return ''

    def graph_stylesheet_callback(self):
        @self.app.callback(Output('graph', 'stylesheet'),
            [Input('slider', 'value'),
            Input('searchbar', 'value')],
            [State('trace-button', 'on')])
        def update_output(slider, search, trace_on):
            if trace_on:
                raise PreventUpdate
            self.view_model.set_range(slider[0], slider[1])
            return self.layout.graph_stylesheet(search)