from dash import Dash
import dash_bootstrap_components as dbc

from persistence.configuration import Configuration
from view import View
from viewmodel.callbacks import CallbackManager
from viewmodel.viewmodel import ViewModel

class App:
    def __init__(self):
        self._configuration = Configuration()
        self._view_model=ViewModel(self._configuration)
        self._view = View(self._view_model)

        self._app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self._app.layout = self._view.layout()

        self.callback_manager = CallbackManager(self._app, self._view_model, self._view)
        self.callback_manager.setup_callbacks()

    def start(self):
        self._app.run_server(debug=True)