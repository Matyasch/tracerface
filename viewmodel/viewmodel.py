from model.base import BaseModel
from model.dynamic import DynamicModel
from model.static import StaticModel

# Transforms data into format usable by the layout
class ViewModel:
    def __init__(self):
        self.model = BaseModel()

    def get_nodes(self):
        return [{'data': {'id': node, 'count': self.model.get_nodes()[node]}} for node in self.model.get_nodes()]

    def get_edges(self):
        return [{'data': {'source': edge[1], 'target': edge[0]}} for edge in self.model.get_edges()]

    def yellow_count(self):
        return round(self.model.yellow_count())

    def red_count(self):
        return round(self.model.red_count())

    def max_count(self):
        return self.model.max_count()

    def output_submit_btn_clicked(self, text):
        self.model = StaticModel()
        self.model.load_text(text)

    def trace_btn_turned_on(self, trace_dict):
        self.model = DynamicModel()
        trace_list = ['{}:{}'.format(app, func) for app, funcs in trace_dict.items() for func in funcs]
        self.model.start_trace(trace_list)

    def trace_btn_turned_off(self):
        self.model.stop_trace()

    def set_range(self, range_bottom, range_top):
        self.model.set_range(range_bottom, range_top)

    def save_config(self, bcc_command):
        self.model.save_config(bcc_command)