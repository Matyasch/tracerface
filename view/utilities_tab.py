import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import view.styles as styles


class UtilitiesTab:
    def __init__(self, view_model):
        self.view_model = view_model

    def search_div(self):
        return dbc.Input(
            id='searchbar',
            type='text',
            placeholder='function name',
            disabled=self.view_model.max_count() < 1)

    def slider_div(self):
        disabled = self.view_model.max_count() < 1
        return dcc.RangeSlider(
            id='slider',
            min=1,
            max=self.view_model.max_count(),
            value=[
                round(self.view_model.model.yellow_count()),
                round(self.view_model.model.red_count())],
            pushable=1,
            disabled=disabled,
            marks={
                1: {'label': '1', 'style': {'color': 'green'}},
                self.view_model.max_count(): {'label': '{}'.format(self.view_model.max_count()), 'style': {'color': 'red'}}},
            tooltip = { 'always_visible': not disabled })

    def tab(self):
        return html.Div(children=[
            dbc.FormGroup([
                dbc.Label('Update coloring'),
                html.Div(
                    id='slider-div',
                    children=self.slider_div(),
                    style={'padding': '40px 0px 20px 0px'})]),
            dbc.FormGroup([
                dbc.Label('Search function', width=4),
                dbc.Col(
                    html.Div(
                        id='search-div',
                        children=self.search_div()),
                    width=8)],
                row=True)],
            style=styles.tab_style())