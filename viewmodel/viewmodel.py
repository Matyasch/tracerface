from model.base import BaseModel
from model.dynamic import DynamicModel
from model.static import StaticModel


# Transforms data into format usable by the layout
class ViewModel:
    def __init__(self, configuration):
        self._model = BaseModel(configuration)
        self._configuration = configuration

    def get_nodes(self):
        return [{
            'data': {
                'id': node,
                'name': self._model.get_nodes()[node]['name'],
                'source': self._model.get_nodes()[node]['source'],
                'count': self._model.get_nodes()[node]['call_count']}
            } for node in self._model.get_nodes()]

    def get_edges(self):
        return [{
            'data': {
                'source': edge[0],
                'target': edge[1],
                'params': self.get_param_visuals_for_edge(edge),
                'call_count': self._model.get_edges()[edge]['call_count'],
                'caller_name': self._model.get_nodes()[edge[0]]['name'],
                'called_name': self._model.get_nodes()[edge[1]]['name']}
            } for edge in self._model.get_edges()]

    def get_param_visuals_for_edge(self, edge):
        calls = self._model.get_edges()[edge]['params']
        if len(calls) == 0:
            return ''
        elif len(calls) == 1:
            return ', '.join(calls[0])
        return '...'

    def get_count_of_edge(self, source, target):
        return self._model.get_edges()[(target, source)]['call_count']

    def get_params_of_edge(self, source, target):
        return self._model.get_edges()[(source, target)]['params']

    def get_params_of_node(self, node_id):
        params_by_functions = [self._model.get_edges()[edge]['params'] for edge in self._model.get_edges() if str(edge[1]) == node_id]
        return [params for calls in params_by_functions for params in calls]

    def yellow_count(self):
        return round(self._model.yellow_count())

    def red_count(self):
        return round(self._model.red_count())

    def max_count(self):
        return self._model.max_count()

    def output_submit_btn_clicked(self, text):
        self._model = StaticModel(self._configuration)
        self._model.load_text(text)

    def trace_with_ui_elements(self, trace_dict):
        self._model = DynamicModel(self._configuration)
        self._model.trace_dict(trace_dict)

    def trace_with_config_file(self, config_path):
        self._model = DynamicModel(self._configuration)
        self._model.trace_yaml(config_path)

    def trace_btn_turned_off(self):
        self._model.stop_trace()

    def set_range(self, range_bottom, range_top):
        self._model.set_range(range_bottom, range_top)

    def save_bcc_command(self, bcc_command):
        self._model.save_bcc_command(bcc_command)

    def save_layout_config(self, animate, spacing):
        self._model.save_layout_config(animate, spacing)

    def get_animate_config(self):
        return self._model.get_animate_config()

    def get_spacing_config(self):
        return self._model.get_spacing_config()

    def thread_error(self):
        return self._model.thread_error()

    def process_error(self):
        return self._model.process_error()

    def trace_active(self):
        return self._model.trace_active()
