import viewmodel.app_dialog_callbacks as app_dialog_callbacks
import viewmodel.configure_callbacks as configure_callbacks
import viewmodel.func_dialog_callbacks as func_dialog_callbacks
import viewmodel.graph_callbacks as graph_callbacks
import viewmodel.realtime_callbacks as realtime_callbacks
import viewmodel.static_callbacks as static_callbacks
import viewmodel.utilities_callbacks as utilities_callbacks


class CallbackManager:
    def __init__(self, app, view_model):
        self.to_trace = {}
        self.setup_callbacks(app, view_model)

    def setup_callbacks(self, app, view_model):
        app_dialog_callbacks.open(app=app)
        app_dialog_callbacks.clear_dialog(app=app)
        app_dialog_callbacks.update_header(app=app)
        app_dialog_callbacks.add_function(app=app, to_trace=self.to_trace)
        app_dialog_callbacks.remove_function(app=app, to_trace=self.to_trace)
        app_dialog_callbacks.update_functions(app=app, to_trace=self.to_trace)
        app_dialog_callbacks.show_func_not_selected_alert(app=app)

        configure_callbacks.save_graph_layout_config(app=app, view_model=view_model)
        configure_callbacks.save_bcc_command_config(app=app, view_model=view_model)

        graph_callbacks.update_graph_elements(app=app, view_model=view_model)
        graph_callbacks.update_graph_style(app=app, view_model=view_model)
        graph_callbacks.display_info_card(app=app, view_model=view_model)

        func_dialog_callbacks.open(app=app)
        func_dialog_callbacks.clear_dialog(app=app)
        func_dialog_callbacks.update_header(app=app)
        func_dialog_callbacks.add_parameter(app=app, to_trace=self.to_trace)
        func_dialog_callbacks.remove_parameter(app=app, to_trace=self.to_trace)
        func_dialog_callbacks.update_parameters(app=app, to_trace=self.to_trace)
        func_dialog_callbacks.show_param_not_selected_alert(app=app)

        realtime_callbacks.start_trace(app=app, view_model=view_model, to_trace=self.to_trace)
        realtime_callbacks.stop_trace_on_error(app=app, view_model=view_model)
        realtime_callbacks.disable_elemts_on_trace(app=app)
        realtime_callbacks.add_application(app=app, to_trace=self.to_trace)
        realtime_callbacks.remove_application(app=app, to_trace=self.to_trace)
        realtime_callbacks.update_apps_dropdown_options(app=app)
        realtime_callbacks.show_app_not_selected_alert(app=app)
        realtime_callbacks.open_config_file_input(app=app)

        static_callbacks.load_output(app=app)

        utilities_callbacks.update_color_slider(app=app, view_model=view_model)
        utilities_callbacks.update_searchbar(app=app, view_model=view_model)