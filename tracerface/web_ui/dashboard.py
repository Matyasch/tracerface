
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

from tracerface.web_ui.dialogs import ManageApplicationDialog, ManageFunctionDialog
from tracerface.web_ui.styles import element_style

# Implementation of the dasboard
class Dashboard(html.Div):
    def __init__(self):
        super().__init__(
            id='dashboard',
            children=[
                self.add_app_group(),
                self.config_path_group(),
                self.manage_apps_group(),
                self.load_output_group(),
                self.trace_group(),
                self.search_function_input(),
                self.slider_group(),
                self.spacing_group(),
                self.animate_checklist(),
                ManageApplicationDialog(),
                ManageFunctionDialog()
            ])

    @staticmethod
    def add_app_group():
        return dbc.FormGroup([
            dbc.Label('Add application to trace', style=element_style()),
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
                style=element_style())
        ])

    @staticmethod
    def manage_apps_group():
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
                style=element_style()),
            dbc.Button('Remove application',
                id='remove-app-button',
                color='danger',
                disabled=True,
                className='mr-1',
                style=element_style()),
            html.Div(
                id='manage-apps-notification',
                children=None,
                style=element_style())
        ])

    @staticmethod
    def trace_group():
        return dbc.FormGroup([
            daq.PowerButton(
                id='trace-button',
                on=False,
                color='#00FF00',
                style=element_style()),
            html.Div(
                id='trace-error-notification',
                children=None,
                style=element_style())
        ])

    @staticmethod
    def config_path_group():
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

    @staticmethod
    def load_output_group():
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
                style=element_style()),
            dcc.Interval(
                id='timer',
                interval=1*500, # in milliseconds
                n_intervals=0,
                disabled=True)
        ])

    @staticmethod
    def slider_group():
        return dbc.FormGroup(
            children=[
                dbc.Label('Update coloring'),
                html.Div(
                    id='slider-div',
                    children=Dashboard.slider(),
                    style={'padding': '40px 0px 20px 0px'})
            ],
            style=element_style())

    @staticmethod
    def search_function_input():
        return dbc.Input(
            id='searchbar',
            type='text',
            disabled=True,
            placeholder='Search function name')

    @staticmethod
    def spacing_group():
        return dbc.FormGroup(
            children=[
                dbc.Label('Spacing between nodes: ', width=7),
                dbc.Col(dbc.Input(
                    id='node-spacing-input',
                    type='number',
                    min=1,
                    value=2))
            ],
            row=True,
            style=element_style())

    @staticmethod
    def animate_checklist():
        return dbc.Checklist(
            options=[{"label": "Animate graph", "value": 'animate'}],
            value=['animate'],
            id="animate-switch",
            switch=True)

    @staticmethod
    def slider(yellow_count=0, red_count=0, max_count=0, disabled=True):
        return dcc.RangeSlider(
            id='slider',
            min=1,
            max=max_count,
            value=[
                round(yellow_count),
                round(red_count)
            ],
            pushable=1,
            disabled=disabled,
            marks={
                1: {'label': '1', 'style': {'color': 'green'}},
                max_count: {'label': '{}'.format(max_count), 'style': {'color': 'red'}}
            },
            tooltip = { 'always_visible': not disabled })
