'''
This module contains all callbacks regarding the utilities tab
'''
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from view.utilities_tab import UtilitiesTab


# Update color slider based on graph and set colors
def update_color_slider(app, view_model):
    @app.callback(Output('slider-div', 'children'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        return UtilitiesTab.slider(view_model.yellow_count(), view_model.red_count(), view_model.max_count())


# Enable or disable searchbar based on whether a graph is present or not
def update_searchbar(app, view_model):
    @app.callback(Output('searchbar', 'disabled'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        return view_model.max_count() < 1
