from dash import Dash

from callback_manager import CallbackManager
from layout import Layout
from viewmodel import ViewModel

class App:
    def __init__(self):
        self._view_model=ViewModel()
        self._layout = Layout(self._view_model)

        self._app = Dash(__name__)
        self._app.layout = self._layout.app_layout()

        self.callback_manager = CallbackManager(self._app, self._view_model, self._layout)
        self.callback_manager.setup_callbacks()

    def start(self):
        self._app.run_server(debug=True)