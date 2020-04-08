'''
This module contains all callbacks regarding
the dialog used to manage functions of an application
'''
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


# Update shown selection of functions for application
# and handling function adding and removal
def update_functions_traced(app, view_model):
    output = Output('functions-traced-select', 'options')
    input = [
        Input('add-function-button', 'n_clicks'),
        Input('remove-func-button', 'n_clicks'),
        Input('applications-select', 'value')
    ]
    state = [
        State('functions-not-traced-select', 'value'),
        State('functions-traced-select', 'value')
    ]
    @app.callback(output, input, state)
    def update_options(add, remove, app, func_to_add, func_to_remove):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]

        if id == 'add-function-button':
            view_model.add_function(app, func_to_add)
        elif id == 'remove-func-button':
            view_model.remove_function(app, func_to_remove)

        functions = view_model.get_traced_functions_for_app(app)
        return [{'label': function, 'value': function} for function in functions]


# Clear values of input elements in dialog
def update_functions_not_traced(app, view_model):
    output = Output('functions-not-traced-select', 'options')
    input = [Input('functions-traced-select', 'options')]
    state = [State('applications-select', 'value')]
    @app.callback(output, input, state)
    def update_options(change, app):
        if app:
            functions = view_model.get_not_traced_functions_for_app(app)
            return [{'label': function, 'value': function} for function in functions]
        return []


# Clear values of input elements in dialog
def clear_traced_dropdown_menu(app):
    output = Output('functions-traced-select', 'value')
    input = [
        Input('remove-func-button', 'n_clicks'),
        Input('app-dialog', 'is_open')
    ]
    @app.callback(output, input)
    def clear_dialog_when_opened(remove, open):
        return None


# Clear values of input elements in dialog
def clear_not_traced_dropdown_menu(app):
    output = Output('functions-not-traced-select', 'value')
    input = [
        Input('add-function-button', 'n_clicks'),
        Input('app-dialog', 'is_open')
    ]
    @app.callback(output, input)
    def clear_dialog_when_opened(add, open):
        return None


# Disable function managagement buttons if no function is selected
def disable_manage_function_buttons(app):
    output = [
        Output('manage-params-button', 'disabled'),
        Output('remove-func-button', 'disabled')
    ]
    input = [Input('functions-traced-select', 'value')]
    @app.callback(output, input)
    def disable(function):
        disabled = not function
        return disabled, disabled


# Disable function managagement buttons if no function is selected
def disable_add_function_button(app):
    output = Output('add-function-button', 'disabled')
    input = [Input('functions-not-traced-select', 'value')]
    @app.callback(output, input)
    def disable(function):
        return not function


# Open dialog window
def open_or_close_dialog(app):
    output = Output('app-dialog', 'is_open')
    input = [
        Input('manage-functions-button', 'n_clicks'),
        Input('close-app-dialog', 'n_clicks')
    ]
    @app.callback(output, input)
    def open_or_close(open, close):
        if not callback_context.triggered:
            raise PreventUpdate
        id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if id == 'manage-functions-button':
            return True
        elif id == 'close-app-dialog':
            return False
        raise PreventUpdate


# Update header of the dialog with the name of the application
def update_header(app):
    output = Output('app-dialog-header', 'children')
    intput = [Input('applications-select', 'value')]
    @app.callback(output, intput)
    def update_app_dialog_header(app):
        if app:
            return 'Manage functions of {}'.format(app)
        raise PreventUpdate
