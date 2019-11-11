from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


def update_color_slider(app, utilities_tab):
    @app.callback(Output('slider-div', 'children'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        if tab == 'utilities-tab':
            return utilities_tab.slider_div()
        return None


def update_searchbar(app, utilities_tab):
    @app.callback(Output('search-div', 'children'),
        [Input('tabs', 'active_tab')])
    def update(tab):
        if tab == 'utilities-tab':
            return utilities_tab.search_div()
        raise PreventUpdate