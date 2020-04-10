import dash_html_components as html
import dash_bootstrap_components as dbc

from view.styles import button_style


# Implementation of Static tab
class StaticTab(dbc.Tab):
    def __init__(self):
        super().__init__(label='Static', tab_id='static-tab', id='static-tab', children=self._content())

    def _content(self):
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
                style=button_style())
        ])
