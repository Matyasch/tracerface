import dash_bootstrap_components as dbc
from dash_html_components import Div

from view.styles import button_style, tab_style


# Implementation of Configure tab
class ConfigureTab(dbc.Tab):
    def __init__(self):
        super().__init__(label='Configure', tab_id='configure-tab', id='configure-tab', children=self._content())

    def _content(self):
        return dbc.FormGroup(
            children=[
                self._command_settings_group(),
                self._graph_settings_group(),
                self._save_changes_group()
            ],
            style=tab_style())

    def _command_settings_group(self):
        return dbc.FormGroup([
            dbc.Label('Command for bcc'),
            dbc.Input(id='bcc-command', type='text', value='trace-bpfcc', placeholder='command')
        ])

    def _graph_settings_group(self):
        return dbc.FormGroup([
            dbc.Checklist(
                    options=[{"label": "Animate graph", "value": 'animate'}],
                    value=['animate'],
                    id="animate-switch",
                    switch=True),
            dbc.FormGroup(children=[
                dbc.Label('Spacing between nodes: ', width=7),
                dbc.Col(
                    dbc.Input(
                        id='node-spacing-input',
                        type='number',
                        min=1,
                        value=2))],
                row=True)
        ])

    def _save_changes_group(self):
        return dbc.FormGroup([
            dbc.Button('Save',
                id='save-config-button',
                color='primary',
                className="mr-1"),
            Div(children=None,
                id='save-config-notification',
                style=button_style())
        ])
