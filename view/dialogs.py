import dash_bootstrap_components as dbc
import dash_html_components as html

from model.utils import format_specs
from view.styles import element_style


class ManageApplicationDialog(dbc.Modal):
    def __init__(self):
        super().__init__(children=self._content(), id='app-dialog')

    def _content(self):
        return [
            dbc.ModalHeader(children=[], id='app-dialog-header'),
            dbc.ModalBody([
                self._add_funtion_group(),
                self._manage_funtions_group(),
            ]),
            dbc.ModalFooter(dbc.Button('Close', id='close-app-dialog', className='ml-auto'))
        ]

    def _add_funtion_group(self):
        return dbc.FormGroup([
            dbc.Label('Add function to trace'),
            dbc.Row([
                dbc.Col(dbc.Input(
                    id='function-name',
                    type='text',
                    placeholder='function name')),
                dbc.Col(
                    dbc.Button('Add',
                        id='add-function-button',
                        color='primary',
                        className='mr-1'),
                    width=2)
            ]),
            dbc.FormText('Write name of the function and click add'),
            html.Div(children=None, id='add-func-notification', style=element_style())
        ])

    def _manage_funtions_group(self):
        return dbc.FormGroup([
            dbc.Label('Manage functions'),
            dbc.Select(
                id='functions-select',
                options=[]),
            dbc.Button('Manage parameters',
                id='manage-params-button',
                color='success',
                className='mr-1',
                style=element_style()),
            dbc.Button('Remove function',
                id='remove-func-button',
                color='danger',
                className='mr-1',
                style=element_style()),
            html.Div(
                id='manage-func-notification',
                children=None,
                style=element_style())
        ])


class ManageFunctionDialog(dbc.Modal):
    def __init__(self):
        super().__init__(children=self._content(), id='func-dialog')

    def _content(self):
        return [
            dbc.ModalHeader(children=[], id='func-dialog-header'),
            dbc.ModalBody([
                self._add_parameter_group(),
                self._manage_parameters_group()
            ]),
            dbc.ModalFooter(dbc.Button('Close', id='close-func-dialog', className='ml-auto'))
        ]

    def _add_parameter_group(self):
        return dbc.FormGroup([
            dbc.Label('Add parameter to trace'),
            dbc.Row([
                dbc.Col(dbc.Select(
                    id='param-type',
                    options=[{
                        "label": format_spec[0], "value": '{}:{}'.format(format_spec[0], format_spec[1])}
                        for format_spec in format_specs()
                    ])),
                dbc.Col(dbc.Input(id='param-index', type='number', min=1)),
                dbc.Col(
                    dbc.Button('Add',
                        id='add-param-button',
                        color='primary',
                        className='mr-1'),
                    width=2)
            ]),
            dbc.FormText('Select the type and the position of the parameter'),
            html.Div(
                id='add-param-notification',
                children=None,
                style=element_style())
        ])

    def _manage_parameters_group(self):
        return dbc.FormGroup([
            dbc.Label('Manage parameters'),
            dbc.Select(
                id='params-select',
                options=[]),
            dbc.Button('Remove parameter',
                id='remove-param-button',
                color='danger',
                className='mr-1',
                style=element_style()),
            html.Div(
                id='remove-param-notification',
                children=None,
                style=element_style())
        ])
