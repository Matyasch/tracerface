#!/usr/bin/env python3

from tracerface.callbacks import (
    app_dialog_callbacks,
    dashboard_callbacks,
    func_dialog_callbacks,
    graph_callbacks
)
from tracerface.trace_controller import TraceController
from tracerface.call_graph import CallGraph
from tracerface.web_ui.layout import Layout
from tracerface.trace_setup import Setup


# Initialize all callbacks used by the application
def _setup_callbacks(app, call_graph, setup, trace_controller):
    app_dialog_callbacks.clear_traced_dropdown_menu(app)
    app_dialog_callbacks.clear_not_traced_dropdown_menu(app)
    app_dialog_callbacks.disable_manage_function_buttons(app)
    app_dialog_callbacks.open_or_close_dialog(app)
    app_dialog_callbacks.update_header(app)
    app_dialog_callbacks.update_functions_traced(app, setup)
    app_dialog_callbacks.update_functions_not_traced(app, setup)

    dashboard_callbacks.disable_searchbar(app, call_graph)
    dashboard_callbacks.disable_manage_app_buttons(app)
    dashboard_callbacks.disable_load_config_button(app)
    dashboard_callbacks.disable_load_button(app)
    dashboard_callbacks.start_or_stop_trace(app, call_graph, setup, trace_controller)
    dashboard_callbacks.stop_trace_on_error(app, trace_controller)
    dashboard_callbacks.clear_selected_app(app)
    dashboard_callbacks.update_apps_dropdown_options(app, setup)
    dashboard_callbacks.update_color_slider(app, call_graph)
    dashboard_callbacks.update_graph_layout(app)

    func_dialog_callbacks.open_or_close_dialog(app)
    func_dialog_callbacks.clear_dialog(app)
    func_dialog_callbacks.update_header(app)
    func_dialog_callbacks.clear_param_select(app)
    func_dialog_callbacks.update_parameters(app, setup)
    func_dialog_callbacks.disable_add_button(app, setup)

    graph_callbacks.update_graph_elements(app, call_graph)
    graph_callbacks.update_graph_style(app, call_graph)

# Initialize all resources used by the application
def initialize(app):
    call_graph = CallGraph()
    trace_controller = TraceController(call_graph)
    setup = Setup()
    app.layout = Layout()
    app.title = 'Tracerface'
    _setup_callbacks(app, call_graph, setup, trace_controller)

