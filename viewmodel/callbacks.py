import json
from pathlib import Path

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import view.alerts as alerts
from view.dialogs import manage_application_dialog, manage_function_dialog

class CallbackManager:
    def __init__(self, app, view_model, layout):
        self.app = app
        self.view_model = view_model
        self.layout = layout
        self.to_trace = {}

    def setup_callbacks(self):
        self.graph_value_callback()
        self.manage_timer_callback()
        self.trace_mode_callback()
        self.slider_visibility_callback()
        self.graph_stylesheet_callback()
        self.config_save_notification_callback()
        self.update_searchbar_callback()
        self.change_app_options_callback()
        self.change_func_options_callback()
        self.open_app_dialog_callback()
        self.open_func_dialog_callback()
        self.change_app_dialog_content_callback()
        self.change_func_dialog_content_callback()
        self.change_params_options_callback()
        self.output_load_notification_callback()
        self.add_app_notification_callback()
        self.change_app_select_value()
        self.change_param_select_value()
        self.info_box_value_callback()
        self.open_config_file_input()
        self.display_node_info_callback()
        self.update_graph_layout_callback()
        self.stop_trace_on_error()
        self.app_not_selected_alert_callback()
        self.add_func_notification()
        self.func_not_selected_alert_callback()
        self.add_param_notification_callback()
        self.remove_param_notification_callback()
        self.change_func_select_value_callback()

    def display_node_info_callback(self):
        @self.app.callback(Output('info-card', 'children'),
            [Input('graph', 'tapNodeData'),
            Input('graph', 'tapEdgeData')])
        def update_node_info(node_data, edge_data):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[1]
            if id == 'tapNodeData' and node_data:
                return self.layout.node_info_card_content(node_data)
            elif id == 'tapEdgeData' and edge_data:
                return self.layout.edge_info_card_content(edge_data)
            raise PreventUpdate

    def info_box_value_callback(self):
        @self.app.callback(Output('info-box', 'children'),
            [Input('tabs', 'active_tab')])
        def update_info(data):
            return json.dumps(self.to_trace, indent=2)

    def graph_value_callback(self):
        @self.app.callback(Output('graph-div', 'children'),
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
            return self.layout.graph()

    def stop_trace_on_error(self):
        @self.app.callback([Output('trace-button', 'on'),
            Output('trace-error-notification', 'children')],
            [Input('timer', 'n_intervals')],
            [State('trace-button', 'on')])
        def stop_trace(timer_tick, trace_on):
            if timer_tick and trace_on:
                if self.view_model.thread_error():
                    return False, alerts.trace_error_alert(self.view_model.thread_error())
                elif self.view_model.process_error():
                    return False, alerts.trace_error_alert(self.view_model.process_error())
                elif not self.view_model.trace_active():
                    return False, alerts.trace_error_alert('Tracing stopped unexpected')
            raise PreventUpdate

    def manage_timer_callback(self):
        @self.app.callback(Output('timer', 'disabled'),
            [Input('trace-button', 'on')],
            [State('timer', 'disabled'),
            State('config-fine-input-collapse', 'is_open'),
            State('config-file-path', 'value')])
        def switch_timer_state(trace_on, disabled, config_use, config_path):
            # TODO: if no functions, don't let turn on
            if trace_on:
                if config_use:
                    self.view_model.trace_with_config_file(config_path)
                else:
                    self.view_model.trace_with_ui_elements(self.to_trace)
            elif not disabled:
                self.view_model.trace_btn_turned_off()
            return not trace_on

    def trace_mode_callback(self):
        @self.app.callback([Output('static-tab', 'disabled'),
            Output('utilities-tab', 'disabled'),
            Output('configure-tab', 'disabled'),
            Output('add-app-button', 'disabled'),
            Output('remove-app-button', 'disabled'),
            Output('manage-functions-button', 'disabled'),
            Output('use-config-file-switch', 'options')],
            [Input('timer', 'disabled')])
        def switch_disables(timer_off):
            # TODO: if no functions, don't let turn on
            trace_on = not timer_off
            return trace_on, trace_on, trace_on, trace_on, trace_on, trace_on, self.layout.config_path_swtich(trace_on)

    def slider_visibility_callback(self):
        @self.app.callback(Output('slider-div', 'children'),
            [Input('tabs', 'active_tab')])
        def show_slider(tab):
            if tab == 'utilities-tab':
                return self.layout.slider_div()
            return None

    def update_searchbar_callback(self):
        @self.app.callback(Output('search-div', 'children'),
            [Input('tabs', 'active_tab')])
        def update_searchbar(tab):
            if tab == 'utilities-tab':
                return self.layout.search_div()
            raise PreventUpdate

    def config_save_notification_callback(self):
        @self.app.callback(Output('save-config-notification', 'children'),
            [Input('save-config-button', 'n_clicks')],
            [State('bcc-command', 'value')])
        def save_clicked(save_btn, bcc_command):
            if save_btn:
                if bcc_command:
                    self.view_model.save_app_config(bcc_command)
                    return alerts.save_config_success_alert()
                else:
                    return alerts.empty_command_config_alert()
            raise PreventUpdate

    def update_graph_layout_callback(self):
        @self.app.callback(Output('graph', 'layout'),
            [Input('save-config-button', 'n_clicks')],
            [State('animate-switch', 'value'),
            State('node-spacing-input', 'value')])
        def update_layout(save_btn, animate_switch, spacing):
            if save_btn:
                animate = len(animate_switch) == 1
                self.view_model.save_layout_config(animate, spacing)
            return self.layout.graph_layout()

    def output_load_notification_callback(self):
        @self.app.callback(Output('load-output-notification', 'children'),
            [Input('submit-button', 'n_clicks')],
            [State('output-textarea', 'value')])
        def submit_clicked(click, content):
            if click:
                if content:
                    return alerts.load_output_success_alert()
                else:
                    return alerts.output_empty_alert()
            raise PreventUpdate

    def add_app_notification_callback(self):
        @self.app.callback(Output('add-app-notification', 'children'),
            [Input('add-app-button', 'n_clicks')],
            [State('application-path', 'value'),
            State('applications-select', 'options')])
        def add_app_clicked(click, path, apps):
            if click:
                if not path:
                    return alerts.empty_app_name_alert()
                if path in [app['value'] for app in apps]:
                    return alerts.app_already_added_alert()
                else:
                    self.to_trace[path] = {}
                    return alerts.add_app_success_alert(app=path)
            raise PreventUpdate

    def graph_stylesheet_callback(self):
        @self.app.callback(Output('graph', 'stylesheet'),
            [Input('slider', 'value'),
            Input('searchbar', 'value')],
            [State('trace-button', 'on')])
        def update_output(slider, search, trace_on):
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
            [State('applications-select', 'value')])
        def add_or_remove_app(remove, selected_app):
            if remove and selected_app:
                if selected_app in self.to_trace:
                    del self.to_trace[selected_app]
                return None
            raise PreventUpdate

    def change_func_select_value_callback(self):
        @self.app.callback(Output('functions-select', 'value'),
            [Input('remove-func-button', 'n_clicks')],
            [State('functions-select', 'value'),
            State('applications-select', 'value')])
        def add_or_remove_function(remove, func, app):
            if remove and func:
                if func in self.to_trace[app]:
                    del self.to_trace[app][func]
                return None
            raise PreventUpdate

    def open_app_dialog_callback(self):
        @self.app.callback(Output('app-dialog', 'is_open'),
            [Input('manage-functions-button', 'n_clicks'),
            Input('close-app-dialog', 'n_clicks')],
            [State('applications-select', 'value')])
        def open_app_dialog(open, close, app):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'manage-functions-button' and open and app:
                return True
            elif id == 'close-app-dialog' and close:
                return False
            raise PreventUpdate

    def open_func_dialog_callback(self):
        @self.app.callback(Output('func-dialog', 'is_open'),
            [Input('manage-params-button', 'n_clicks'),
            Input('close-func-dialog', 'n_clicks')],
            [State('functions-select', 'value')])
        def open_func_dialog(open_click, close_click, function):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'manage-params-button' and open_click and function:
                return True
            elif id == 'close-func-dialog' and close_click:
                return False
            raise PreventUpdate

    def func_not_selected_alert_callback(self):
        @self.app.callback(Output('manage-func-notification', 'children'),
            [Input('manage-params-button', 'n_clicks'),
            Input('remove-func-button', 'n_clicks')],
            [State('functions-select', 'value')])
        def show_manage_funcs_alert(open_click, remove_click, function):
            if (open_click or remove_click) and not function:
                return alerts.no_func_selected_alert()
            raise PreventUpdate

    def app_not_selected_alert_callback(self):
        @self.app.callback(Output('manage-apps-notification', 'children'),
            [Input('manage-functions-button', 'n_clicks'),
            Input('remove-app-button', 'n_clicks')],
            [State('applications-select', 'value')])
        def show_manage_apps_alert(open_click, remove_click, app):
            if (open_click or remove_click) and not app:
                return alerts.no_app_selected_alert()
            raise PreventUpdate

    def add_func_notification(self):
        @self.app.callback(Output('add-func-notification', 'children'),
            [Input('add-function-button', 'n_clicks')],
            [State('function-name', 'value'),
            State('functions-select', 'options')])
        def show_add_func_alert(add_click, name, functions):
            if add_click and name and name not in [function['label'] for function in functions]:
                return alerts.func_add_success_alert()
            elif add_click and name and name in [function['label'] for function in functions]:
                return alerts.function_already_added_alert()
            elif add_click and not name:
                return alerts.empty_function_name_alert()
            raise PreventUpdate

    def change_app_dialog_content_callback(self):
        @self.app.callback(Output('app-dialog', 'children'),
            [Input('applications-select', 'value')])
        def change_app_dialog(app):
            if app:
                functions = self.to_trace[app] or []
                return manage_application_dialog(app, functions)
            raise PreventUpdate

    def change_func_dialog_content_callback(self):
        @self.app.callback(Output('func-dialog', 'children'),
            [Input('functions-select', 'value')],
            [State('applications-select', 'value')])
        def change_app_dialog(func, app):
            if func:
                params = self.to_trace[app][func] or []
                return manage_function_dialog(func=func, options=['{} : {}'.format(param, params[param]) for param in params])
            raise PreventUpdate

    def change_func_options_callback(self):
        @self.app.callback(Output('functions-select', 'options'),
            [Input('add-function-button', 'n_clicks'),
            Input('remove-func-button', 'n_clicks')],
            [State('function-name', 'value'),
            State('functions-select', 'options'),
            State('functions-select', 'value'),
            State('applications-select', 'value')])
        def add_or_remove_function(manage, remove, name, functions, selected_func, app):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'add-function-button' and manage and name and name not in [function['label'] for function in functions]:
                self.to_trace[app][name] = {}
                return functions + [{'label': name, 'value': name}]
            if id == 'remove-func-button' and remove and selected_func:
                return [func for func in functions if func['value'] != selected_func]
            raise PreventUpdate

    def add_param_notification_callback(self):
        @self.app.callback(Output('add-param-notification', 'children'),
            [Input('add-param-button', 'n_clicks')],
            [State('param-index', 'value'),
            State('param-type', 'value'),
            State('params-select', 'options')])
        def show_alert(add, index, format_spec, params):
            if add:
                if not format_spec:
                    return alerts.no_param_type_alert()
                elif not index:
                    return alerts.no_param_index_alert()
                elif 'arg{}'.format(index) in [param['label'].split(' : ')[0] for param in params]:
                    return alerts.param_already_added_alert()
                else:
                    return alerts.param_add_success_alert()
            raise PreventUpdate

    def remove_param_notification_callback(self):
        @self.app.callback(Output('remove-param-notification', 'children'),
            [Input('remove-param-button', 'n_clicks')],
            [State('params-select', 'value')])
        def show_alert(remove, function):
            if remove and not function:
                return alerts.no_param_selected_alert()
            raise PreventUpdate

    def change_params_options_callback(self):
        @self.app.callback(Output('params-select', 'options'),
            [Input('add-param-button', 'n_clicks'),
            Input('remove-param-button', 'n_clicks')],
            [State('param-index', 'value'),
            State('param-type', 'value'),
            State('params-select', 'options'),
            State('params-select', 'value'),
            State('functions-select', 'value'),
            State('applications-select', 'value')])
        def add_or_remove_parameter(add, remove, index, format_spec, params, selected_param, func, app):
            context = dash.callback_context
            if not context.triggered:
                raise PreventUpdate
            id = context.triggered[0]['prop_id'].split('.')[0]
            if id == 'add-param-button' and add and format_spec and index and 'arg{}'.format(index) not in [param['label'].split(' : ')[0] for param in params]:
                self.to_trace[app][func]['arg{}'.format(index)] = format_spec.split(':')[1]
                return params + [{'label': 'arg{} : {}'.format(index, format_spec.split(':')[1]), 'value': (index, format_spec)}]
            if id == 'remove-param-button' and selected_param:
                del self.to_trace[app][func]['arg{}'.format(selected_param[0])]
                return [param for param in params if param['label'].split(' : ')[0] != 'arg{}'.format(selected_param[0])]
            raise PreventUpdate

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

    def change_param_select_value(self):
        @self.app.callback(Output('params-select', 'value'),
            [Input('remove-param-button', 'n_clicks')],
            [State('params-select', 'value')])
        def add_or_remove_app(remove, selected_param):
            if remove and selected_param:
                return None
            raise PreventUpdate

    def open_config_file_input(self):
        @self.app.callback(Output('config-fine-input-collapse', 'is_open'),
            [Input('use-config-file-switch', 'value')])
        def open_config_collapse(open):
            return len(open) == 1