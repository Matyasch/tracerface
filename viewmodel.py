# Transforms data into format usable by the layout
class ViewModel:
    def __init__(self, model):
        self.model = model

    def get_nodes(self):
        return [{'data': {'id': node, 'count': self.model.get_nodes()[node]}} for node in self.model.get_nodes()]

    def get_edges(self):
        return [{'data': {'source': edge[1], 'target': edge[0]}} for edge in self.model.get_edges()]

    def green_count(self):
        return self.model.green_count()

    def yellow_count(self):
        return self.model.yellow_count()

    def red_count(self):
        return self.model.red_count()

    def output_submit_button_clicked(self, text):
        self.model.initialize_from_text(text)