from model.base import BaseModel
from model.dynamic import DynamicModel
from model.static import StaticModel


# Transforms data into format usable by the layout
class ViewModel:
    def __init__(self):
        self.model = BaseModel()

    def get_nodes(self):
        return [{
        'data': {
            'id': node,
            'name': self.model.get_nodes()[node]['name'],
            'source': self.model.get_nodes()[node]['source'],
            'count': self.model.get_nodes()[node]['call_count']}
        } for node in self.model.get_nodes()]

    def get_edges(self):
        return [{
                'data': {
                    'source': edge[0],
                    'target': edge[1],
                    'params': self.get_param_visuals_for_edge(edge),
                    'call_count': self.model.get_edges()[edge]['call_count'],
                    'caller_name': self.model.get_nodes()[edge[0]]['name'],
                    'called_name': self.model.get_nodes()[edge[1]]['name']
                }
            } for edge in self.model.get_edges()]

    def get_param_visuals_for_edge(self, edge):
        calls = self.model.get_edges()[edge]['params']
        if len(calls) == 0:
            return ''
        elif len(calls) == 1:
            return ', '.join(calls[0])
        return '...'

    def get_count_of_edge(self, source, target):
        return self.model.get_edges()[(target, source)]['call_count']

    def get_params_of_edge(self, source, target):
        return self.model.get_edges()[(source, target)]['params']

    def get_params_of_node(self, node_id):
        params_by_functions = [self.model.get_edges()[edge]['params'] for edge in self.model.get_edges() if str(edge[1]) == node_id]
        return [params for calls in params_by_functions for params in calls]

    def yellow_count(self):
        return round(self.model.yellow_count())

    def red_count(self):
        return round(self.model.red_count())

    def max_count(self):
        return self.model.max_count()

    def output_submit_btn_clicked(self, text):
        self.model = StaticModel()
        self.model.load_text(text)

    def trace_with_ui_elements(self, trace_dict):
        self.model = DynamicModel()
        self.model.trace_dict(trace_dict)

    def trace_with_config_file(self, config_path):
        self.model = DynamicModel()
        self.model.trace_config_file(config_path)

    def trace_btn_turned_off(self):
        self.model.stop_trace()

    def set_range(self, range_bottom, range_top):
        self.model.set_range(range_bottom, range_top)

    def save_app_config(self, bcc_command):
        self.model.save_app_config(bcc_command)

    def save_layout_config(self, animate, spacing):
        self.model.save_layout_config(animate, spacing)

    def animate_config(self):
        return self.model.get_animate_config()

    def spacing_config(self):
        return self.model.get_spacing_config()