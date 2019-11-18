import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import view.styles as styles


class UtilitiesTab(dbc.Tab):
    def __init__(self):
        super().__init__(label='Utilities', tab_id='utilities-tab', id='utilities-tab', children=self.content())

    @staticmethod
    def slider(yellow_count=0, red_count=0, max_count=0):
        disabled = max_count < 1
        return dcc.RangeSlider(
            id='slider',
            min=1,
            max=max_count,
            value=[
                round(yellow_count),
                round(red_count)],
            pushable=1,
            disabled=disabled,
            marks={
                1: {'label': '1', 'style': {'color': 'green'}},
                max_count: {'label': '{}'.format(max_count), 'style': {'color': 'red'}}},
            tooltip = { 'always_visible': not disabled })

    def content(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Update coloring'),
                html.Div(
                    id='slider-div',
                    children=self.slider(),
                    style={'padding': '40px 0px 20px 0px'})]),
            dbc.FormGroup([
                dbc.Label('Search function:'),
                dbc.Col(
                    dbc.Input(
                        id='searchbar',
                        type='text',
                        placeholder='function name'),
                    width=8)],
                row=True)],
            style=styles.tab_style())