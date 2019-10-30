from persistence.configuration import Configuration
from persistence.persistence import Persistence

# Manages logic and persistence
class BaseModel:
    def __init__(self):
        self._persistence = Persistence()
        self._configuration = Configuration()
        self.debug = ''

    # Returns a list of nodes and their call count
    def get_nodes(self):
        return self._persistence.nodes

    # Returns a list of edges and their frequency
    def get_edges(self):
        return self._persistence.edges

    def yellow_count(self):
        return self._persistence.get_range().yellow

    def red_count(self):
        return self._persistence.get_range().red

    def max_count(self):
        return self._persistence.get_range().top

    def set_range(self, yellow, red):
        self._persistence.update_color_range(yellow, red)

    def save_config(self, bcc_command):
        self._configuration = Configuration(bcc_command=bcc_command)