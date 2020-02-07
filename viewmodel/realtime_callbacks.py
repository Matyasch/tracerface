'''
This module contains all callbacks regarding the realtime tracing
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import view.alerts as alerts
from view.realtime_tab import RealtimeTab


# Stop tracing if an error occurs
def stop_trace_on_error(app, view_model):
    @app.callback([Output('trace-button', 'on'),
        Output('trace-error-notification', 'children')],
        [Input('timer', 'n_intervals')],
        [State('trace-button', 'on')])
    def stop_trace(timer_tick, trace_on):
        if timer_tick and trace_on:
            if view_model.thread_error():
                return False, alerts.trace_error_alert(view_model.thread_error())
            elif view_model.process_error():
                return False, alerts.trace_error_alert(view_model.process_error())
            elif not view_model.trace_active():
                return False, alerts.trace_error_alert('Tracing stopped unexpected')
        raise PreventUpdate


# Start realtime tracing
def start_trace(app, view_model, to_trace):
    @app.callback(Output('timer', 'disabled'),
        [Input('trace-button', 'on')],
        [State('timer', 'disabled'),
        State('config-file-input-collapse', 'is_open'),
        State('config-file-path', 'value')])
    def switch_state(trace_on, disabled, config_use, config_path):
        # TODO: if no functions, don't let turn on
        if trace_on:
            if config_use:
                view_model.trace_with_config_file(config_path)
            else:
                view_model.trace_with_ui_elements(to_trace)
        elif not disabled:
            view_model.trace_btn_turned_off()
        return not trace_on


# Disable parts of the interface while tracing is active
def disable_interface_on_trace(app):
    @app.callback([Output('static-tab', 'disabled'),
        Output('utilities-tab', 'disabled'),
        Output('add-app-button', 'disabled'),
        Output('remove-app-button', 'disabled'),
        Output('manage-functions-button', 'disabled'),
        Output('use-config-file-switch', 'options')],
        [Input('timer', 'disabled')])
    def switch_disables(timer_off):
        trace_on = not timer_off
        return trace_on, trace_on, trace_on, trace_on, trace_on, RealtimeTab.config_path_swtich(trace_on)


# Add or remove application to trace
def update_apps_dropdown_options(app):
    @app.callback(Output('applications-select', 'options'),
        [Input('add-app-button', 'n_clicks'),
        Input('remove-app-button', 'n_clicks')],
        [State('application-path', 'value'),
        State('applications-select', 'options'),
        State('applications-select', 'value')])
    def update_options(add, remove, path, apps, selected_app):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'add-app-button' and add and path and path not in [app['value'] for app in apps]:
            return apps + [{"label": path, "value": path}]
        elif id == 'remove-app-button' and remove and selected_app:
            return [app for app in apps if app['label'] != selected_app]
        return apps


# Update value of application selection on application removal
def remove_application(app, to_trace):
    @app.callback(Output('applications-select', 'value'),
        [Input('remove-app-button', 'n_clicks')],
        [State('applications-select', 'value')])
    def update_value(remove, selected_app):
        if remove and selected_app:
            if selected_app in to_trace:
                del to_trace[selected_app]
            return None
        raise PreventUpdate


# Show notification when adding application to trace
def show_add_application_alert(app, to_trace):
    @app.callback(Output('add-app-notification', 'children'),
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
                to_trace[path] = {}
                return alerts.add_app_success_alert(app=path)
        raise PreventUpdate


# Show notification when trying to remove application without selecting it
def show_app_not_selected_alert(app):
    @app.callback(Output('manage-apps-notification', 'children'),
        [Input('manage-functions-button', 'n_clicks'),
        Input('remove-app-button', 'n_clicks')],
        [State('applications-select', 'value')])
    def show_manage_apps_alert(open_click, remove_click, app):
        if (open_click or remove_click) and not app:
            return alerts.no_app_selected_alert()
        raise PreventUpdate


# Show input element for config file path
def open_config_file_input(app):
    @app.callback(Output('config-file-input-collapse', 'is_open'),
        [Input('use-config-file-switch', 'value')])
    def open_config_collapse(config):
        return len(config) == 1
