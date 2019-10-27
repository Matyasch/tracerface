import json
from pathlib import Path

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

class CallbackManager:
    def __init__(self, app, view_model, layout):
        self.app = app
        self.view_model = view_model
        self.layout = layout
        self.functions_to_trace = []

    def setup_callbacks(self):
        self.graph_value_callback()
        self.timer_disabled_callback()
        self.slider_visibility_callback()
        self.graph_stylesheet_callback()
        self.config_save_notification_callback()
        self.static_tab_disabled_callback()
        self.utilities_tab_disabled_callback()
        self.searchbar_disabled_callback()
        self.add_app_callback()
        self.open_app_dialog_callback()
        self.change_app_dialog_content_callback()
        self.add_func_callback()
        self.output_load_notification_callback()
        self.info_box_value_callback()

    def info_box_value_callback(self):
        @self.app.callback(Output('info-box', 'children'),
            [Input('add-app-button', 'n_clicks')],
            [State('application-path', 'value'),
            State('applications-select', 'options')])
        def update_info(n_clicks, path, apps):
            if path:
                app = Path(path).name
                return str(self.functions_to_trace)
            return apps

    def graph_value_callback(self):
        @self.app.callback(Output('graph_div', 'children'),
            [Input('submit-button', 'n_clicks'),
            Input('timer', 'n_intervals')],
            [State('output-textarea', 'value')])
        def update_graph(out_btn, n_int, output):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'submit-button' and output:
                self.view_model.output_submit_btn_clicked(output)
            return self.layout.graph_layout()

    def timer_disabled_callback(self):
        @self.app.callback(Output('timer', 'disabled'),
            [Input('trace-button', 'on')],
            [State('timer', 'disabled')])
        def switch_timer_state(trace_on, disabled):
            # TODO: if no functions, don't let turn on
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            if trace_on:
                self.view_model.trace_btn_turned_on(self.functions_to_trace)
            elif not disabled:
                self.view_model.trace_btn_turned_off()
            return not trace_on

    def slider_visibility_callback(self):
        @self.app.callback(Output('slider-div', 'children'),
            [Input('tabs', 'active_tab')])
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
            [Input('tabs', 'active_tab')])
        def disable_searchbar(tab):
            return tab == 'utilities-tab' and not self.view_model.max_count() > 0

    def utilities_tab_disabled_callback(self):
        @self.app.callback(Output('utilities-tab', 'disabled'),
            [Input('trace-button', 'on')])
        def disable_utilities_tab(trace_on):
            return trace_on

    def config_save_notification_callback(self):
        @self.app.callback(Output('save-config-notification', 'children'),
            [Input('save-config-button', 'n_clicks')],
            [State('bcc-command', 'value')])
        def save_clicked(save_btn, bcc_command):
            if save_btn:
                if bcc_command:
                    self.view_model.save_config(bcc_command)
                    return self.layout.save_config_alert(success=True)
                else:
                    return self.layout.save_config_alert(success=False)
            else:
                return ''

    def output_load_notification_callback(self):
        @self.app.callback(Output('load-output-notification', 'children'),
            [Input('submit-button', 'n_clicks')],
            [State('output-textarea', 'value')])
        def save_clicked(click, content):
            if click:
                if content:
                    return self.layout.load_output_alert(success=True)
                else:
                    return self.layout.load_output_alert(success=False)
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

    def add_app_callback(self):
        @self.app.callback(Output('applications-select', 'options'),
            [Input('add-app-button', 'n_clicks'),
            Input('remove-app-button', 'n_clicks')],
            [State('application-path', 'value'),
            State('applications-select', 'options'),
            State('applications-select', 'value')])
        def add_application(add_app, remove, path, apps, selected_app):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'add-app-button' and path and path not in [app['value'] for app in apps]:
                return apps + [{"label": Path(path).name, "value": path}]
            elif id == 'remove-app-button' and selected_app:
                self.functions_to_trace = [func for func in self.functions_to_trace if func.split(':')[0] != selected_app]
                return [app for app in apps if app['label'] != selected_app]
            return apps

    def open_app_dialog_callback(self):
        @self.app.callback(Output('app-dialog', 'is_open'),
            [Input('add-function-button', 'n_clicks'),
            Input('close-app-dialog', 'n_clicks')],
            [State('applications-select', 'value'),
            State('functions-select', 'options')])
        def open_app_dialog(open, close, app, functions):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'add-function-button':
                return True
            elif id == 'close-app-dialog':
                if functions:
                    self.functions_to_trace += ['{}:{}'.format(app, func['value']) for func in functions]
                return False

    def change_app_dialog_content_callback(self):
        @self.app.callback(Output('app-dialog', 'children'),
            [Input('applications-select', 'value')])
        def change_app_dialog(app):
            if not app:
                raise PreventUpdate
            functions = [func.split(':')[1] for func in self.functions_to_trace if func.split(':')[0] == app]
            return self.layout.manage_application_dialog(app, functions)

    def add_func_callback(self):
        @self.app.callback(Output('functions-select', 'options'),
            [Input('add-func-button', 'n_clicks')],
            [State('function-name', 'value'),
            State('functions-select', 'options')])
        def add_function(add, name, functions):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'add-func-button':
                return functions + [{"label": name, "value": name}]