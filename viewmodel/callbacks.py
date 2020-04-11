'''
Initialize all shared resources used by callbacks
Initialize all callbacks used by the application
'''
import viewmodel.app_dialog_callbacks as app_dialog_callbacks
import viewmodel.func_dialog_callbacks as func_dialog_callbacks
import viewmodel.graph_callbacks as graph_callbacks
import viewmodel.realtime_callbacks as realtime_callbacks
import viewmodel.utilities_callbacks as utilities_callbacks


class CallbackManager:
    def __init__(self, app, view_model):
        self.setup_callbacks(app, view_model)

    def setup_callbacks(self, app, view_model):
        app_dialog_callbacks.clear_traced_dropdown_menu(app=app)
        app_dialog_callbacks.clear_not_traced_dropdown_menu(app=app)
        app_dialog_callbacks.disable_manage_function_buttons(app=app)
        app_dialog_callbacks.disable_add_function_button(app=app)
        app_dialog_callbacks.open_or_close_dialog(app=app)
        app_dialog_callbacks.update_header(app=app)
        app_dialog_callbacks.update_functions_traced(app=app, view_model=view_model)
        app_dialog_callbacks.update_functions_not_traced(app=app, view_model=view_model)

        graph_callbacks.update_graph_elements(app=app, view_model=view_model)
        graph_callbacks.update_graph_style(app=app, view_model=view_model)
        graph_callbacks.display_info_card(app=app, view_model=view_model)

        func_dialog_callbacks.open_or_close_dialog(app=app)
        func_dialog_callbacks.clear_dialog(app=app)
        func_dialog_callbacks.update_header(app=app)
        func_dialog_callbacks.clear_param_select(app=app)
        func_dialog_callbacks.update_parameters(app=app, view_model=view_model)
        func_dialog_callbacks.disable_add_button(app=app, view_model=view_model)

        realtime_callbacks.disable_interface_on_trace(app=app)
        realtime_callbacks.disable_add_app_button(app=app, view_model=view_model)
        realtime_callbacks.disable_manage_app_buttons(app=app)
        realtime_callbacks.disable_load_config_button(app=app)
        realtime_callbacks.disable_load_button(app=app)
        realtime_callbacks.start_or_stop_trace(app=app, view_model=view_model)
        realtime_callbacks.stop_trace_on_error(app=app, view_model=view_model)
        realtime_callbacks.clear_selected_app(app=app)
        realtime_callbacks.update_apps_dropdown_options(app=app, view_model=view_model)

        utilities_callbacks.update_color_slider(app=app, view_model=view_model)
        utilities_callbacks.update_searchbar(app=app, view_model=view_model)
        utilities_callbacks.update_graph_layout(app=app, view_model=view_model)
