from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from callbacks import (
    app_dialog_callbacks,
    dashboard_callbacks,
    func_dialog_callbacks,
    graph_callbacks
)
from model.trace_controller import TraceController
from persistence.call_graph import CallGraph
from view.layout import Layout
from viewmodel.trace_setup import Setup
from viewmodel.viewmodel import ViewModel


# Class to store the application's resources
class App:
    def __init__(self):
        self._call_graph = CallGraph()
        self._trace_controller = TraceController(self._call_graph)
        self._setup = Setup()
        self._view_model = ViewModel(self._call_graph, self._setup, self._trace_controller)
        self._app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
        self._app.layout = Layout()
        self._app.title = 'Tracerface'

        self._setup_callbacks(
            app=self._app,
            view_model=self._view_model,
            call_graph=self._call_graph,
            setup=self._setup,
            trace_controller=self._trace_controller)

    # Start server of the web application
    def start(self, debug, logging):
        silent = not logging
        try:
            self._app.run_server(debug=debug, dev_tools_silence_routes_logging=silent)
        except OSError:
            print('Address already in use!\nDid you already start the application?')
            exit(1)

    # Initialize all callbacks used by the application
    def _setup_callbacks(self, app, view_model, call_graph, setup, trace_controller):
        app_dialog_callbacks.clear_traced_dropdown_menu(app=app)
        app_dialog_callbacks.clear_not_traced_dropdown_menu(app=app)
        app_dialog_callbacks.disable_manage_function_buttons(app=app)
        app_dialog_callbacks.open_or_close_dialog(app=app)
        app_dialog_callbacks.update_header(app=app)
        app_dialog_callbacks.update_functions_traced(app=app, setup=setup)
        app_dialog_callbacks.update_functions_not_traced(app=app, setup=setup)

        dashboard_callbacks.disable_searchbar(app=app, call_graph=call_graph)
        dashboard_callbacks.disable_manage_app_buttons(app=app)
        dashboard_callbacks.disable_load_config_button(app=app)
        dashboard_callbacks.disable_load_button(app=app)
        dashboard_callbacks.start_or_stop_trace(app=app, call_graph=call_graph,
                                                setup=setup, trace_controller=trace_controller)
        dashboard_callbacks.stop_trace_on_error(app=app, trace_controller=trace_controller)
        dashboard_callbacks.clear_selected_app(app=app)
        dashboard_callbacks.update_apps_dropdown_options(app=app, setup=setup)
        dashboard_callbacks.update_color_slider(app=app, call_graph=call_graph)
        dashboard_callbacks.update_graph_layout(app=app)

        func_dialog_callbacks.open_or_close_dialog(app=app)
        func_dialog_callbacks.clear_dialog(app=app)
        func_dialog_callbacks.update_header(app=app)
        func_dialog_callbacks.clear_param_select(app=app)
        func_dialog_callbacks.update_parameters(app=app, setup=setup)
        func_dialog_callbacks.disable_add_button(app=app, setup=setup)

        graph_callbacks.update_graph_elements(app=app, view_model=view_model, call_graph=call_graph)
        graph_callbacks.update_graph_style(app=app, view_model=view_model, call_graph=call_graph)
