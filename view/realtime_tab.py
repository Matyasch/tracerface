import dash_bootstrap_components as dbc
from dash_core_components import Interval
import dash_daq as daq
import dash_html_components as html

from view.dialogs import ManageApplicationDialog, ManageFunctionDialog
import view.styles as styles


# Implementation of Realtime tab
class RealtimeTab(dbc.Tab):
    def __init__(self):
        super().__init__(label='Realtime', tab_id='realtime-tab', id='realtime-tab', children=self._content(), tab_style={"margin-left": "auto"})

    def _content(self):
        return html.Div(
            children=[
                self._add_app_group(),
                self._manage_apps_group(),
                self._config_path_group(),
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
                    width=2)]),
            dbc.FormText('Write path to runnable and click add'),
            html.Div(
                id='add-app-notification',
                children=None,
                style=styles.button_style())
        ])

    def _manage_apps_group(self):
        return dbc.FormGroup([
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
                dbc.Checklist(
                    options=self.config_path_swtich(),
                    value=[],
                    id="use-config-file-switch",
                    switch=True),
                dbc.Collapse(
                    dbc.Input(
                        id='config-file-path',
                        type='text',
                        placeholder='/path/to/config'),
                    id="config-file-input-collapse")
            ],
            style=styles.button_style())

    def _timer(self):
        return Interval(
            id='timer',
            interval=1*500, # in milliseconds
            n_intervals=0,
            disabled=True)

    @staticmethod
    def config_path_swtich(disabled=False):
        return [{"label": "Use config file instead", "value": 'config', 'disabled': disabled}]
