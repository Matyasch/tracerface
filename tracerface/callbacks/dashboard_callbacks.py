'''
This module contains all callbacks regarding the realtime tracing
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from  tracerface.web_ui.alerts import (
    ErrorAlert,
    SuccessAlert,
    TraceErrorAlert,
    WarningAlert
)
from tracerface.web_ui.dashboard import Dashboard
from tracerface.web_ui.graph import Graph
from tracerface.web_ui.trace_setup import (
    BinaryAlreadyAddedError,
    BinaryNotExistsError,
    ConfigFileError,
    FunctionNotInBinaryError
)


# Disable function managagement buttons if no function is selected
def disable_manage_app_buttons(app):
    output = [
        Output('manage-functions-button', 'disabled'),
        Output('remove-app-button', 'disabled')
    ]
    input = [Input('applications-select', 'value')]
    @app.callback(output, input)
    def disable(app):
        disabled = not app
        return disabled, disabled


# Disable config load button if no path is provided
def disable_load_config_button(app):
    output = Output('load-config-button', 'disabled')
    input = [Input('config-file-path', 'value')]
    @app.callback(output, input)
    def disable(path):
        return not path


# Load output of bcc trace output
def disable_load_button(app):
    output = Output('load-output-button', 'disabled')
    input = [Input('output-path', 'value')]
    @app.callback(output, input)
    def disable(content):
        return not content


# Stop tracing if an error occurs
def stop_trace_on_error(app, trace_controller):
    output = [
        Output('trace-button', 'on'),
        Output('trace-error-notification', 'children')
    ]
    input = [Input('timer', 'n_intervals')]
    state = [State('trace-button', 'on')]
    @app.callback(output, input, state)
    def stop_trace(timer_tick, trace_on):
        if timer_tick and trace_on:
            if trace_controller.thread_error():
                return False, TraceErrorAlert(trace_controller.thread_error())
        raise PreventUpdate


# Start realtime tracing
def start_or_stop_trace(app, call_graph, setup, trace_controller):
    output = Output('timer', 'disabled')
    input = [Input('trace-button', 'on')]
    state = [State('timer', 'disabled')]
    @app.callback(output, input, state)
    def switch_state(trace_on, timer_disabled):
        if trace_on:
            call_graph.clear()
            trace_controller.start_trace(setup.generate_bcc_args(), call_graph)
        elif not timer_disabled:
            trace_controller.stop_trace()
        return not trace_on


# Update color slider based on graph and set colors
def update_color_slider(app, call_graph):
    output = Output('slider-div', 'children')
    input = [
        Input('graph', 'elements'),
        Input('timer', 'disabled')
    ]
    @app.callback(output, input)
    def update(elements, timer_off):
        if not callback_context.triggered:
            raise PreventUpdate

        disabled = call_graph.max_count() < 1 or not timer_off
        return Dashboard.slider(call_graph.get_yellow(), call_graph.get_red(),
                                call_graph.max_count(), disabled)


# Disable parts of the interface while tracing is active
def disable_searchbar(app, call_graph):
    output = Output('searchbar', 'disabled')
    input = [
        Input('graph', 'elements'),
        Input('timer', 'disabled')
    ]
    @app.callback(output, input)
    def switch_disables(elements, timer_off):
        disabled = call_graph.max_count() < 1 or not timer_off
        return disabled


# Update collection of apps to be traced
def update_apps_dropdown_options(app, setup):
    output = [
        Output('applications-select', 'options'),
        Output('add-app-notification', 'children')
    ]
    input = [
        Input('add-app-button', 'n_clicks'),
        Input('remove-app-button', 'n_clicks'),
        Input('load-config-button', 'n_clicks')
    ]
    state = [
        State('application-path', 'value'),
        State('applications-select', 'value'),
        State('config-file-path', 'value')
    ]
    @app.callback(output, input, state)
    def update_options(add, remove, load, app_to_add, app_to_remove, config_path):
        if not callback_context.triggered:
            raise PreventUpdate

        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        alert = None

        if id == 'add-app-button' and app_to_add:
            try:
                setup.initialize_binary(app_to_add)
                alert = SuccessAlert('Application added')
            except BinaryNotExistsError:
                msg = 'Binary not found at given path so it is assumed to be a built-in function'
                alert = WarningAlert(msg)
                setup.initialize_built_in(app_to_add)
        elif id == 'remove-app-button' and app_to_remove:
            setup.remove_app(app_to_remove)
        elif id == 'load-config-button' and config_path:
            try:
                err_message = setup.load_from_file(config_path)
                if err_message:
                    alert = WarningAlert(err_message)
                else:
                    alert = SuccessAlert('Setup loaded')
            except (BinaryAlreadyAddedError, ConfigFileError, FunctionNotInBinaryError) as e:
                alert = ErrorAlert(str(e))
        return [{"label": app, "value": app} for app in setup.get_apps()], alert


# Update value of application selection on application removal
def clear_selected_app(app):
    output = Output('applications-select', 'value')
    input = [
        Input('remove-app-button', 'n_clicks'),
        Input('add-app-button', 'n_clicks')
    ]
    @app.callback(output, input)
    def clear_value(add, remove):
        if add or remove:
            return None
        raise PreventUpdate


# Save animation status and spacing between nodes
def update_graph_layout(app):
    output = Output('graph', 'layout')
    input = [
        Input('animate-switch', 'value'),
        Input('node-spacing-input', 'value')
    ]
    @app.callback(output, input)
    def update_spacing_and_animate(animate_switch, spacing):
        animate = len(animate_switch) == 1
        return Graph.layout(spacing=spacing, animate=animate)
