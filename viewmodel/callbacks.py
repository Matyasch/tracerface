import viewmodel.app_dialog_callbacks as app_dialog_callbacks
import viewmodel.configure_callbacks as configure_callbacks
import viewmodel.func_dialog_callbacks as func_dialog_callbacks
import viewmodel.graph_callbacks as graph_callbacks
import viewmodel.realtime_callbacks as realtime_callbacks
import viewmodel.static_callbacks as static_callbacks
import viewmodel.utilities_callbacks as utilities_callbacks


class CallbackManager:
    def __init__(self, app, view_model, layout):
        self.app = app
        self.view_model = view_model
        self.layout = layout
        self.to_trace = {}

    def setup_callbacks(self):
        app_dialog_callbacks.open(app=self.app)
        app_dialog_callbacks.update(app=self.app, to_trace=self.to_trace)
        app_dialog_callbacks.add_function(app=self.app, to_trace=self.to_trace)
        app_dialog_callbacks.remove_function(app=self.app, to_trace=self.to_trace)
        app_dialog_callbacks.update_funcs_dropdown_options(app=self.app)
        app_dialog_callbacks.show_func_not_selected_alert(app=self.app)

        configure_callbacks.save_graph_layout_config(app=self.app, view_model=self.view_model, graph=self.layout.graph)
        configure_callbacks.save_bcc_command_config(app=self.app, view_model=self.view_model)

        graph_callbacks.update_graph_value(app=self.app, view_model=self.view_model, graph=self.layout.graph)
        graph_callbacks.update_graph_style(app=self.app, view_model=self.view_model, graph=self.layout.graph)
        graph_callbacks.display_info_card(app=self.app, view_model=self.view_model)

        func_dialog_callbacks.open(app=self.app)
        func_dialog_callbacks.update(app=self.app, to_trace=self.to_trace)
        func_dialog_callbacks.add_parameter(app=self.app, to_trace=self.to_trace)
        func_dialog_callbacks.remove_parameter(app=self.app, to_trace=self.to_trace)
        func_dialog_callbacks.update_params_dropdown_options(app=self.app)
        func_dialog_callbacks.show_param_not_selected_alert(app=self.app)

        realtime_callbacks.start_trace(app=self.app, view_model=self.view_model, to_trace=self.to_trace)
        realtime_callbacks.stop_trace_on_error(app=self.app, view_model=self.view_model)
        realtime_callbacks.disable_elemts_on_trace(app=self.app, realtime_tab=self.layout.dashboard.realtime)
        realtime_callbacks.add_application(app=self.app, to_trace=self.to_trace)
        realtime_callbacks.remove_application(app=self.app, to_trace=self.to_trace)
        realtime_callbacks.update_apps_dropdown_options(app=self.app)
        realtime_callbacks.show_app_not_selected_alert(app=self.app)
        realtime_callbacks.open_config_file_input(app=self.app)

        static_callbacks.load_output(app=self.app)

        utilities_callbacks.update_color_slider(app=self.app, view_model=self.view_model)
        utilities_callbacks.update_searchbar(app=self.app, view_model=self.view_model)