from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def show_submit_alert(app):
    @app.callback(Output('load-output-notification', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('output-textarea', 'value')])
    def show_alert(click, content):
        if click:
            if content:
                return alerts.load_output_success_alert()
            else:
                return alerts.output_empty_alert()
        raise PreventUpdate