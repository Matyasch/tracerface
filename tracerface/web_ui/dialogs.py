import dash_bootstrap_components as dbc
import dash_core_components as dcc

from tracerface.web_ui.styles import element_style


# Format specifiers and their labels to show for parameters
FORMAT_SPECS = [
    ('char', '%c'),
    ('double/float', '%f'),
    ('int', '%d'),
    ('long', '%l'),
    ('long double', '%lF'),
    ('string/char *', '%s'),
    ('short', '%hi'),
    ('unsigned short', '%hi'),
    ('void *', '%p'),
]


# Implementation of dialog window to manage an application
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
                dbc.Col(dcc.Dropdown(
                    id='functions-not-traced-select',
                    placeholder='Select function to set it traced')),
                dbc.Col(
                    dbc.Button('Add',
                        id='add-function-button',
                        color='primary',
                        className='mr-1'),
                    width=2)
            ]),
            dbc.FormText('Write name of the function and click add')
        ])

    def _manage_funtions_group(self):
        return dbc.FormGroup([
            dbc.Label('Manage functions'),
            dcc.Dropdown(
                id='functions-traced-select',
                placeholder='Select function to manage'),
            dbc.Button('Manage parameters',
                id='manage-params-button',
                color='success',
                className='mr-1',
                style=element_style()),
            dbc.Button('Remove function',
                id='remove-func-button',
                color='danger',
                className='mr-1',
                style=element_style())
        ])


# Implementation of dialog window to manage a function
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
                        "label": format_spec[0], "value": format_spec[1]}
                            for format_spec in FORMAT_SPECS
                    ])),
                dbc.Col(dbc.Input(id='param-index', type='number', min=1)),
                dbc.Col(
                    dbc.Button('Add',
                        id='add-param-button',
                        color='primary',
                        className='mr-1'),
                    width=2)
            ]),
            dbc.FormText('Select the type and the position of the parameter')
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
                style=element_style())
        ])
