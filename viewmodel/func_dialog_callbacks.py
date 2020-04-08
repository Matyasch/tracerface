'''
This module contains all callbacks regarding
the dialog used to manage parameters of a function
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


# Open dialog window
def open_or_close_dialog(app):
    output = Output('func-dialog', 'is_open')
    input = [
        Input('manage-params-button', 'n_clicks'),
        Input('close-func-dialog', 'n_clicks')
    ]
    @app.callback(output, input)
    def open_or_close(open, close):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]

        if id == 'manage-params-button':
            return True
        elif id == 'close-func-dialog':
            return False
        raise PreventUpdate


# Clear values of input elements in dialog
def clear_dialog(app):
    output = [
        Output('param-type', 'value'),
        Output('param-index', 'value')
    ]
    input = [Input('func-dialog', 'is_open')]
    @app.callback(output, input)
    def clear_dialog_when_opened(open):
        return None, None


# Update name of function to configure in header
def update_header(app):
    output = Output('func-dialog-header', 'children')
    input = [Input('functions-traced-select', 'value')]
    @app.callback(output, input)
    def update_func_dialog(func):
        return 'Manage parameters of {}'.format(func)


# Update shown selection of parameters for function
# and handle adding or removing parameter for tracing
def update_parameters(app, view_model):
    output = Output('params-select', 'options')
    input = [
        Input('add-param-button', 'n_clicks'),
        Input('remove-param-button', 'n_clicks'),
        Input('functions-traced-select', 'value')
    ]
    state = [
        State('param-index', 'value'),
        State('param-type', 'value'),
        State('params-select', 'value'),
        State('applications-select', 'value')
    ]
    @app.callback(output, input, state)
    def add_param(add, remove, function, index, format, param_to_remove, app):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]

        if id == 'add-param-button' and index not in view_model.get_parameters(app, function):
            view_model.add_parameter(app, function, index, format)
        elif id == 'remove-param-button':
            view_model.remove_parameter(app, function, param_to_remove)

        parameters = view_model.get_parameters(app, function)
        return [
            {
                'label': 'arg{} : {}'.format(index, parameters[index]),
                'value': index
            } for index in parameters
        ]


# Remove parameter from traced ones for function
def clear_param_select(app):
    output = Output('params-select', 'value')
    input = [Input('remove-param-button', 'n_clicks')]
    @app.callback(output, input)
    def remove_param(remove):
        return None


# Show alert if no parameter is selected while trying to remove one
def disable_add_button(app, view_model):
    output = Output('add-param-button', 'disabled')
    input = [
        Input('param-index', 'value'),
        Input('param-type', 'value'),
        Input('params-select', 'options')
    ]
    state = [
        State('functions-traced-select', 'value'),
        State('applications-select', 'value')
    ]
    @app.callback(output, input, state)
    def disable(index, format, options_changed, function, app):
        valid = format and index and int(index) not in view_model.get_parameters(app, function)
        return not valid
