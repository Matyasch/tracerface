import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

from view.dialogs import manage_application_dialog, manage_function_dialog
import view.styles as styles


class Tabs:
    def __init__(self, view_model):
        self.view_model = view_model

    def search_div(self):
        return [dbc.Input(
            id='searchbar',
            type='text',
            placeholder='function name',
            disabled=self.view_model.max_count() < 1)]

    def slider_div(self):
        disabled = self.view_model.max_count() < 1
        return [dcc.RangeSlider(
                    id='slider',
                    min=1,
                    max=self.view_model.max_count(),
                    value=[round(self.view_model.model.yellow_count()), round(self.view_model.model.red_count())],
                    pushable=1,
                    disabled=disabled,
                    marks={
                        1: {'label': '1', 'style': {'color': 'green'}},
                        self.view_model.max_count(): {'label': '{}'.format(self.view_model.max_count()), 'style': {'color': 'red'}}
                    },
                    tooltip = { 'always_visible': not disabled })]

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

    def config_path_swtich(self, disabled=False):
        return [{"label": "Use config file instead", "value": 'config', 'disabled': disabled}]

    def static_tab(self):
        return html.Div([
            dbc.FormGroup([
                dbc.Label('Trace output'),
                dbc.Textarea(
                    id='output-textarea',
                    placeholder='Enter trace output',
                    style={'height': '200px'}),
                dbc.Button('Submit',
                    id='submit-button',
                    color='primary',
                    className='mr-1',
                    style=styles.button_style()),
                html.Div(
                    id='load-output-notification',
                    children=None,
                    style=styles.button_style())
            ])
        ],
        style=styles.tab_style())

    def realtime_tab(self):
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

    def utilities_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Update coloring'),
                html.Div(
                    id='slider-div',
                    children=self.slider_div(),
                    style={'padding': '40px 0px 20px 0px'}
                )]),
            dbc.FormGroup([
                dbc.Label('Search function', width=4),
                dbc.Col(
                    html.Div(
                        id='search-div',
                        children=self.search_div()),
                    width=8)
            ],
            row=True)
        ],
        style=styles.tab_style())

    def configure_tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Command for bcc: ', width=5),
                dbc.Col(
                    dbc.Input(
                        id='bcc-command',
                        type='text',
                        value='trace-bpfcc',
                        placeholder='command',
                    ))
                ],
                row=True),
            dbc.Checklist(
                options=[
                    {"label": "Animate graph", "value": 'animate'}
                ],
                value=['animate'],
                id="animate-switch",
                switch=True),
            dbc.FormGroup([
                dbc.Label('Spacing between nodes: ', width=7),
                dbc.Col(
                    dbc.Input(
                        id='node-spacing-input',
                        type='number',
                        min=1,
                        value=2))
                ],
                row=True),
            dbc.Button('Save',
                id='save-config-button',
                color='primary',
                className="mr-1"),
            html.Div(
                id='save-config-notification',
                children=None,
                style=styles.button_style())
        ],
        style=styles.tab_style())