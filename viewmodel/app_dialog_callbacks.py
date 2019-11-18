from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import view.alerts as alerts


def update_functions(app, to_trace):
    @app.callback(Output('functions-select', 'options'),
        [Input('add-function-button', 'n_clicks'),
        Input('remove-func-button', 'n_clicks'),
        Input('applications-select', 'value')],
        [State('function-name', 'value'),
        State('functions-select', 'options'),
        State('functions-select', 'value')])
    def change_options(manage, remove, app, func_name, functions, selected_func):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'add-function-button' and manage and func_name and func_name not in [function['label'] for function in functions]:
            return functions + [{'label': func_name, 'value': func_name}]
        elif id == 'remove-func-button' and remove and selected_func:
            return [func for func in functions if func['value'] != selected_func]
        elif id == 'applications-select' and app:
            options = to_trace[app] or []
            return [{"label": name, "value": name} for name in options]
        raise PreventUpdate


def open(app):
    @app.callback(Output('app-dialog', 'is_open'),
        [Input('manage-functions-button', 'n_clicks'),
        Input('close-app-dialog', 'n_clicks')],
        [State('applications-select', 'value')])
    def open_app_dialog(open, close, app):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'manage-functions-button' and open and app:
            return True
        elif id == 'close-app-dialog' and close:
            return False
        raise PreventUpdate


def update_header(app):
    @app.callback(Output('app-dialog-header', 'children'),
        [Input('applications-select', 'value')])
    def update_app_dialog_header(app):
        if app:
            return 'Manage functions of {}'.format(app)
        raise PreventUpdate


def add_function(app, to_trace):
    @app.callback(Output('add-func-notification', 'children'),
        [Input('add-function-button', 'n_clicks')],
        [State('function-name', 'value'),
        State('functions-select', 'options'),
        State('applications-select', 'value')])
    def show_add_func_alert(add_click, name, functions, app):
        if add_click:
            if not name:
                return alerts.empty_function_name_alert()
            elif name in [function['label'] for function in functions]:
                return alerts.function_already_added_alert()
            else:
                to_trace[app][name] = {}
                return alerts.func_add_success_alert(name)
        raise PreventUpdate


def remove_function(app, to_trace):
    @app.callback(Output('functions-select', 'value'),
        [Input('remove-func-button', 'n_clicks')],
        [State('functions-select', 'value'),
        State('applications-select', 'value')])
    def add_or_remove_function(remove, func, app):
        if remove and func:
            if func in to_trace[app]:
                del to_trace[app][func]
            return None
        raise PreventUpdate


def show_func_not_selected_alert(app):
    @app.callback(Output('manage-func-notification', 'children'),
        [Input('manage-params-button', 'n_clicks'),
        Input('remove-func-button', 'n_clicks')],
        [State('functions-select', 'value')])
    def show_manage_funcs_alert(open_click, remove_click, function):
        if (open_click or remove_click) and not function:
            return alerts.no_func_selected_alert()
        raise PreventUpdate