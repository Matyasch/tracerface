'''
Parent class of the two types of models used.
Provides basic functionality and persistence handling.
'''


class BaseModel:
    def __init__(self, persistence):
        self._persistence = persistence

    # returns all nodes in a list
    def get_nodes(self):
        return self._persistence.get_nodes()

    # returns all edges in a list
    def get_edges(self):
        return self._persistence.get_edges()

    # returns the lower bound for coloring elements yellow
    def yellow_count(self):
        return self._persistence.get_yellow()

    # returns the lower bound for coloring elements red
    def red_count(self):
        return self._persistence.get_red()

    # returns the maximum number of calls among nodes
    def max_count(self):
        call_counts = [node['call_count'] for node in self._persistence.get_nodes().values()]
        if call_counts:
            return max(call_counts)
        return 0

    # set new values for the coloring bounds
    def set_range(self, yellow, red):
        self._persistence.update_colors(yellow, red)

    # initialize color boundaries to default values based on maximum count
    def init_colors(self):
        yellow = round(self.max_count()/3)
        red = round(self.max_count()*2/3)
        self._persistence.update_colors(yellow, red)
