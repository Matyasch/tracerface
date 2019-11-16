from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from view.utilities_tab import UtilitiesTab


def update_color_slider(app, view_model):
    @app.callback(Output('slider-div', 'children'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        return UtilitiesTab.slider(view_model.yellow_count(), view_model.red_count(), view_model.max_count())


def update_searchbar(app, view_model):
    @app.callback(Output('searchbar', 'disabled'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        return view_model.max_count() < 1