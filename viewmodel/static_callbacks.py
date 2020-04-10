'''
This module contains all callbacks regarding static processing
'''
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import view.alerts as alerts


# Load output of bcc trace output
def disable_load_button(app):
    output = Output('load-output-button', 'disabled')
    input = [Input('output-path', 'value')]
    @app.callback(output, input)
    def disable(content):
        return not content
