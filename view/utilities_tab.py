import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import view.styles as styles


# Implementation of Utilities tab
class UtilitiesTab(dbc.Tab):
    def __init__(self):
        super().__init__(label='Utilities', tab_id='utilities-tab',
                         id='utilities-tab', children=self._content())

    def _content(self):
        return html.Div(
            children=[
                self._coloring_group(),
                self._func_name_input(),
                self._spacing_group(),
                self._animate_checklist()
            ],
            style=styles.tab_style())

    def _coloring_group(self):
        return dbc.FormGroup(
            children=[
                dbc.Label('Update coloring'),
                html.Div(
                    id='slider-div',
                    children=self.slider(),
                    style={'padding': '40px 0px 20px 0px'})
            ],
            style=styles.element_style())

    def _func_name_input(self):
        return dbc.Input(
            id='searchbar',
            type='text',
            placeholder='Search function name')

    def _spacing_group(self):
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
            style=styles.element_style())

    def _animate_checklist(self):
        return dbc.Checklist(
            options=[{"label": "Animate graph", "value": 'animate'}],
            value=['animate'],
            id="animate-switch",
            switch=True)

    @staticmethod
    def slider(yellow_count=0, red_count=0, max_count=0):
        disabled = max_count < 1
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
