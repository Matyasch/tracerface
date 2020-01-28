from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import view.alerts as alerts


def open(app):
    @app.callback(Output('func-dialog', 'is_open'),
        [Input('manage-params-button', 'n_clicks'),
        Input('close-func-dialog', 'n_clicks')],
        [State('functions-select', 'value')])
    def open_func_dialog(open_click, close_click, function):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'manage-params-button' and open_click and function:
            return True
        elif id == 'close-func-dialog' and close_click:
            return False
        raise PreventUpdate


def clear_dialog(app):
    @app.callback([Output('param-type', 'value'),
        Output('param-index', 'value')],
        [Input('func-dialog', 'is_open')])
    def clear_dialog_when_opened(open):
        return None, ''


def update_header(app):
    @app.callback(Output('func-dialog-header', 'children'),
        [Input('functions-select', 'value')])
    def update_func_dialog(func):
        if func:
            return 'Manage parameters of {}'.format(func)
        raise PreventUpdate


def update_parameters(app, to_trace):
    @app.callback(Output('params-select', 'options'),
        [Input('add-param-button', 'n_clicks'),
        Input('remove-param-button', 'n_clicks'),
        Input('functions-select', 'value')],
        [State('param-index', 'value'),
        State('param-type', 'value'),
        State('params-select', 'options'),
        State('params-select', 'value'),
        State('applications-select', 'value')])
    def add_param(add, remove, selected_func, index, format_spec, params, selected_param, selected_app):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'add-param-button' and add and format_spec and index and 'arg{}'.format(index) not in [param['label'].split(' : ')[0] for param in params]:
            return params + [{'label': 'arg{} : {}'.format(index, format_spec.split(':')[1]), 'value': (index, format_spec)}]
        elif id == 'remove-param-button' and selected_param:
            return [param for param in params if param['label'].split(' : ')[0] != 'arg{}'.format(selected_param[0])]
        elif id == 'functions-select' and selected_func and selected_app:
            params = to_trace[selected_app][selected_func] or []
            return [{"label": '{} : {}'.format(name, params[name]), "value": (int(name.split('arg')[1]), params[name])} for name in params]
        raise PreventUpdate


def remove_parameter(app, to_trace):
    @app.callback(Output('params-select', 'value'),
        [Input('remove-param-button', 'n_clicks'),
        Input('func-dialog', 'is_open')],
        [State('params-select', 'value'),
        State('functions-select', 'value'),
        State('applications-select', 'value')])
    def remove_param(remove, open, selected_param, func, app):
        if remove and selected_param:
            param_name = 'arg{}'.format(selected_param[0])
            if param_name in to_trace[app][func]:
                del to_trace[app][func][param_name]
        return None


def add_parameter(app, to_trace):
    @app.callback(Output('add-param-notification', 'children'),
        [Input('add-param-button', 'n_clicks')],
        [State('param-index', 'value'),
        State('param-type', 'value'),
        State('params-select', 'options'),
        State('functions-select', 'value'),
        State('applications-select', 'value')])
    def show_alert(add, index, format_spec, params, func, app):
        if add:
            if not format_spec:
                return alerts.no_param_type_alert()
            elif not index:
                return alerts.no_param_index_alert()
            elif 'arg{}'.format(index) in [param['label'].split(' : ')[0] for param in params]:
                return alerts.param_already_added_alert()
            else:
                to_trace[app][func]['arg{}'.format(index)] = format_spec.split(':')[1]
                return alerts.param_add_success_alert()
        raise PreventUpdate


def show_param_not_selected_alert(app):
    @app.callback(Output('remove-param-notification', 'children'),
        [Input('remove-param-button', 'n_clicks')],
        [State('params-select', 'value')])
    def show_alert(remove, function):
        if remove and not function:
            return alerts.no_param_selected_alert()
        raise PreventUpdate