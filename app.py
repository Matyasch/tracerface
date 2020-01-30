from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from persistence.configuration import Configuration
from view.layout import Layout
from viewmodel.callbacks import CallbackManager
from viewmodel.viewmodel import ViewModel


# Class to store the application's resources
class App:
    def __init__(self):
        self._configuration = Configuration()
        self._view_model = ViewModel(self._configuration)
        self._app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
        self._app.layout = Layout()
        self._app.title = 'Tracerface'

        self.callback_manager = CallbackManager(self._app, self._view_model)

    # Start server of the web application
    def start(self, debug, logging):
        silent = not logging
        try:
            self._app.run_server(debug=debug, dev_tools_silence_routes_logging=silent)
        except OSError as e:
            print('Address already in use!\nDid you already start the application?')
            exit(1)
