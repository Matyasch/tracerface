from dash import Dash

from callback_manager import CallbackManager
from layout import Layout

class View:
    def __init__(self, view_model):
        self.view_model=view_model
        self.layout = Layout(self.view_model)

        self.app = Dash(__name__)
        self.app.layout = self.layout.app_layout()

        self.callback_manager = CallbackManager(self.app, self.view_model)
        self.callback_manager.setup_callbacks()