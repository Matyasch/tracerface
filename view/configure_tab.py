import dash_bootstrap_components as dbc
from dash_html_components import Div

from view.styles import button_style, tab_style


class ConfigureTab:
    def tab(self):
        return Div(children=[
            dbc.FormGroup(children=[
                dbc.Label('Command for bcc: ', width=5),
                dbc.Col(dbc.Input(
                    id='bcc-command',
                    type='text',
                    value='trace-bpfcc',
                    placeholder='command'))],
                row=True),
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
                row=True),
            dbc.Button('Save',
                id='save-config-button',
                color='primary',
                className="mr-1"),
            Div(children=None,
                id='save-config-notification',
                style=button_style())],
            style=tab_style())