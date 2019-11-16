from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from view.utilities_tab import UtilitiesTab


def update_color_slider(app, view_model):
    @app.callback(Output('slider-div', 'children'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        if tab == 'utilities-tab':
            return UtilitiesTab.slider_div(view_model.yellow_count(), view_model.red_count(), view_model.max_count())
        return None


def update_searchbar(app, view_model):
    @app.callback(Output('search-div', 'children'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        if tab == 'utilities-tab':
            return UtilitiesTab.search_div(view_model.max_count())
        raise PreventUpdate