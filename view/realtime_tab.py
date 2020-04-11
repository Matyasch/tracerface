import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

from view.dialogs import ManageApplicationDialog, ManageFunctionDialog
import view.styles as styles


# Implementation of Realtime tab
class RealtimeTab(dbc.Tab):
    def __init__(self):
        super().__init__(label='Tools', tab_id='realtime-tab', id='realtime-tab',
                         children=self._content(), tab_style={"margin-left": "auto"})

    def _content(self):
        return html.Div(
            children=[
                self._add_app_group(),
                self._config_path_group(),
                self._manage_apps_group(),
                self._load_output_group(),
                self._trace_group(),
                self._timer(),
                ManageApplicationDialog(),
                ManageFunctionDialog()
            ],
            style=styles.tab_style())

    def _add_app_group(self):
        return dbc.FormGroup([
            dbc.Label('Add application to trace'),
            dbc.Row([
                dbc.Col(dbc.Input(
                    id='application-path',
                    type='text',
                    placeholder='/path/to/binary')),
                dbc.Col(dbc.Button('Add',
                    id='add-app-button',
                    color='primary',
                    className='mr-1'),
                    width=2)
            ]),
            html.Div(
                id='add-app-notification',
                children=None,
                style=styles.button_style())
        ])

    def _manage_apps_group(self):
        return dbc.FormGroup([
            dbc.Label('Manage applications'),
            dcc.Dropdown(
                id='applications-select',
                placeholder='Select application to manage'),
            dbc.Button('Manage functions',
                id='manage-functions-button',
                color='success',
                disabled=True,
                className='mr-1',
                style=styles.button_style()),
            dbc.Button('Remove application',
                id='remove-app-button',
                color='danger',
                disabled=True,
                className='mr-1',
                style=styles.button_style()),
            html.Div(
                id='manage-apps-notification',
                children=None,
                style=styles.button_style())
        ])

    def _trace_group(self):
        return dbc.FormGroup([
            daq.PowerButton(
                id='trace-button',
                on=False,
                color='#00FF00',
                style=styles.button_style()),
            html.Div(
                id='trace-error-notification',
                children=None,
                style=styles.button_style())
        ])

    def _config_path_group(self):
        return dbc.FormGroup(
            children=[
                dbc.Label('Load setup from file'),
                dbc.Row([
                    dbc.Col(dbc.Input(
                        id='config-file-path',
                        type='text',
                        placeholder='/path/to/config')),
                    dbc.Col(dbc.Button('Load',
                        id='load-config-button',
                        color='primary',
                        className='mr-1'),
                        width=2)
                ])
            ])

    def _load_output_group(self):
        return dbc.FormGroup([
            dbc.Label('Load output of BCC trace run'),
            dbc.Row([
                dbc.Col(dbc.Input(
                    id='output-path',
                    type='text',
                    placeholder='/path/to/file')),
                dbc.Col(dbc.Button('Load',
                    id='load-output-button',
                    color='primary',
                    className='mr-1'),
                    width=2)
            ]),
            html.Div(
                id='load-output-notification',
                children=None,
                style=styles.button_style())
        ])

    def _timer(self):
        return dcc.Interval(
            id='timer',
            interval=1*500, # in milliseconds
            n_intervals=0,
            disabled=True)

    @staticmethod
    def config_path_swtich(disabled=False):
        return [{
            "label": "Use config file instead",
            "value": 'config',
            'disabled': disabled
        }]
