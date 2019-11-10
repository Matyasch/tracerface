import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_html_components as html

from view.dialogs import manage_application_dialog, manage_function_dialog
import view.styles as styles


class RealtimeTab:
    def config_path_swtich(self, disabled=False):
        return [{"label": "Use config file instead", "value": 'config', 'disabled': disabled}]

    def config_path_div(self):
        return [
            dbc.Checklist(
                options=self.config_path_swtich(),
                value=[],
                id="use-config-file-switch",
                switch=True,
            ),
            dbc.Collapse(
                dbc.Input(
                    id='config-file-path',
                    type='text',
                    placeholder='/path/to/config'
                ),
                id="config-fine-input-collapse",
            )
        ]

    def tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Add application to trace'),
                dbc.Row([
                    dbc.Col(dbc.Input(
                        id='application-path',
                        type='text',
                        placeholder='/path/to/binary'
                    )),
                    dbc.Col(dbc.Button('Add',
                        id='add-app-button',
                        color='primary',
                        className='mr-1'),
                    width=2)
                ]),
                dbc.FormText('Write path to runnable and click add'),
                html.Div(
                    id='add-app-notification',
                    children=None,
                    style=styles.button_style())
            ]),
            dbc.FormGroup([
                dbc.Label('Manage applications'),
                dbc.Select(
                    id='applications-select',
                    options=[]),
                dbc.Button('Manage functions',
                    id='manage-functions-button',
                    color='success',
                    className='mr-1',
                    style=styles.button_style()),
                dbc.Button('Remove application',
                    id='remove-app-button',
                    color='danger',
                    className='mr-1',
                    style=styles.button_style()),
                html.Div(
                    id='manage-apps-notification',
                    children=None,
                    style=styles.button_style())
                ]),
            html.Div(
                id='config-path-div',
                children=self.config_path_div(),
                style=styles.button_style()),
            daq.PowerButton(
                id='trace-button',
                on=False,
                color='#00FF00'),
            html.Div(
                id='trace-error-notification',
                children=None,
                style=styles.button_style()),
            dbc.Modal(children=manage_application_dialog(),
                id='app-dialog',
                scrollable=True),
            dbc.Modal(children=manage_function_dialog(),
                id='func-dialog',
                scrollable=True)
        ],
        style=styles.tab_style())