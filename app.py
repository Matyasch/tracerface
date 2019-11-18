from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from persistence.configuration import Configuration
from view.layout import Layout
from viewmodel.callbacks import CallbackManager
from viewmodel.viewmodel import ViewModel


class App:
    def __init__(self):
        self._configuration = Configuration()
        self._view_model = ViewModel(self._configuration)
        self._app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
        self._app.layout = Layout()
        self._app.title = 'Tracerface'

        self.callback_manager = CallbackManager(self._app, self._view_model)

    def start(self):
        self._app.run_server(dev_tools_silence_routes_logging=True)