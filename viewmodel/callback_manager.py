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
        self.to_trace = {}

    def setup_callbacks(self):
        self.graph_value_callback()
        self.timer_disabled_callback()
        self.slider_visibility_callback()
        self.graph_stylesheet_callback()
        self.config_save_notification_callback()
        self.static_tab_disabled_callback()
        self.utilities_tab_disabled_callback()
        self.searchbar_disabled_callback()
        self.change_app_options_callback()
        self.change_func_options_callback()
        self.open_app_dialog_callback()
        self.change_app_dialog_content_callback()
        self.output_load_notification_callback()
        self.add_app_notification_callback()
        self.change_app_select_value()
        self.info_box_value_callback()

    def info_box_value_callback(self):
        @self.app.callback(Output('info-box', 'children'),
            [Input('add-app-button', 'n_clicks')],
            [State('application-path', 'value'),
            State('applications-select', 'options')])
        def update_info(n_clicks, path, apps):
            if path:
                return str(['{}:{}'.format(app, func) for app, funcs in self.to_trace.items() for func in funcs])
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
                self.view_model.trace_btn_turned_on(self.to_trace)
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
        def submit_clicked(click, content):
            if click:
                if content:
                    return self.layout.load_output_alert(success=True)
                else:
                    return self.layout.load_output_alert(success=False)
            else:
                return ''

    def add_app_notification_callback(self):
        @self.app.callback(Output('add-app-notification', 'children'),
            [Input('add-app-button', 'n_clicks')],
            [State('application-path', 'value'),
            State('applications-select', 'options')])
        def add_app_clicked(click, path, apps):
            if click:
                if path and path not in [app['value'] for app in apps]:
                    return self.layout.add_app_alert(success=True, app=path)
                else:
                    return self.layout.add_app_alert(success=False)
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

    def change_app_options_callback(self):
        @self.app.callback(Output('applications-select', 'options'),
            [Input('add-app-button', 'n_clicks'),
            Input('remove-app-button', 'n_clicks')],
            [State('application-path', 'value'),
            State('applications-select', 'options'),
            State('applications-select', 'value')])
        def add_or_remove_app(add, remove, path, apps, selected_app):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'add-app-button' and add and path and path not in [app['value'] for app in apps]:
                return apps + [{"label": path, "value": path}]
            elif id == 'remove-app-button' and remove and selected_app:
                return [app for app in apps if app['label'] != selected_app]
            return apps

    def change_app_select_value(self):
        @self.app.callback(Output('applications-select', 'value'),
            [Input('remove-app-button', 'n_clicks')],
            [State('applications-select', 'value'),
            State('applications-select', 'options')])
        def add_or_remove_app(remove, selected_app, apps):
            if remove and selected_app:
                if selected_app in self.to_trace:
                    del self.to_trace[selected_app]
                return None
            raise PreventUpdate

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
            if id == 'add-function-button' and open:
                return True
            elif id == 'close-app-dialog' and close:
                if functions:
                    self.to_trace[app] = [func['value'] for func in functions]
                return False

    def change_app_dialog_content_callback(self):
        @self.app.callback(Output('app-dialog', 'children'),
            [Input('applications-select', 'value')])
        def change_app_dialog(app):
            if not app:
                raise PreventUpdate
            functions = self.to_trace[app] if app in self.to_trace else []
            return self.layout.manage_application_dialog(app, functions)

    def change_func_options_callback(self):
        @self.app.callback(Output('functions-select', 'options'),
            [Input('add-func-button', 'n_clicks'),
            Input('remove-func-button', 'n_clicks')],
            [State('function-name', 'value'),
            State('functions-select', 'options'),
            State('functions-select', 'value')])
        def add_or_remove_function(add, remove, name, functions, selected_func):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'add-func-button' and name:
                return functions + [{"label": name, "value": name}]
            if id == 'remove-func-button' and selected_func:
                return [func for func in functions if func['value'] != selected_func]

    def change_func_select_value(self):
        @self.app.callback(Output('functions-select', 'value'),
            [Input('remove-func-button', 'n_clicks')],
            [State('applications-select', 'value'),
            State('functions-select', 'value')])
        def add_or_remove_app(remove, selected_app, selected_func):
            if remove and selected_func:
                if selected_func in self.to_trace[selected_app]:
                    self.to_trace[selected_app].remove(selected_func)
                return None
            raise PreventUpdate