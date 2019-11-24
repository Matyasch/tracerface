from persistence.persistence import Persistence


# Manages logic and persistence
class BaseModel:
    def __init__(self, configuration):
        self._persistence = Persistence()
        self._configuration = configuration

    def get_nodes(self):
        return self._persistence.get_nodes()

    def get_edges(self):
        return self._persistence.get_edges()

    def yellow_count(self):
        return self._persistence.get_yellow()

    def red_count(self):
        return self._persistence.get_red()

    def max_count(self):
        call_counts = [node['call_count'] for node in self._persistence.get_nodes().values()]
        if call_counts:
            return max(call_counts)
        return 0

    def set_range(self, yellow, red):
        self._persistence.update_colors(yellow, red)

    def save_app_config(self, bcc_command):
        self._configuration.update_command(bcc_command)

    def save_layout_config(self, animate, spacing):
        self._configuration.update_layout(animate, spacing)

    def get_spacing_config(self):
        return self._configuration.get_spacing()

    def get_animate_config(self):
        return self._configuration.get_animate()

    def init_colors(self):
        yellow = round(self.max_count()/3)
        red = round(self.max_count()*2/3)
        self._persistence.update_colors(yellow, red)