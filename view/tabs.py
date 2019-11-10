from view.configure_tab import ConfigureTab
from view.static_tab import StaticTab
from view.realtime_tab import RealtimeTab
from view.utilities_tab import UtilitiesTab


class Tabs:
    def __init__(self, view_model):
        self.view_model = view_model
        self.configure_tab = ConfigureTab()
        self.static_tab = StaticTab()
        self.realtime_tab = RealtimeTab()
        self.utilities_tab = UtilitiesTab(view_model)

    def static(self):
        return self.static_tab.tab()

    def realtime(self):
        return self.realtime_tab.tab()

    def utilities(self):
        return self.utilities_tab.tab()

    def configure(self):
        return self.configure_tab.tab()