from model.base import BaseModel
from model.dynamic import DynamicModel
from model.static import StaticModel


# Transforms data into format usable by the layout
class ViewModel:
    def __init__(self):
        self._model = BaseModel()

    # Return list of nodes in a format usable to the view
    def get_nodes(self):
        return [{
            'data': {
                'id': node,
                'name': self._model.get_nodes()[node]['name'],
                'source': self._model.get_nodes()[node]['source'],
                'count': self._model.get_nodes()[node]['call_count']}
            } for node in self._model.get_nodes()]

    # Return list of edges in a format usable to the view
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

    # Return label of a given edge based on its parameters
    def get_param_visuals_for_edge(self, edge):
        calls = self._model.get_edges()[edge]['params']
        if len(calls) == 0:
            return ''
        elif len(calls) == 1:
            return ', '.join(calls[0])
        return '...'

    # Return parameters for an edge defined by its source and target
    def get_params_of_edge(self, source, target):
        return self._model.get_edges()[(source, target)]['params']

    # Return parameters for a node defined by its id/hash
    def get_params_of_node(self, node_id):
        params_by_functions = [self._model.get_edges()[edge]['params'] for edge in self._model.get_edges() if str(edge[1]) == node_id]
        return [params for calls in params_by_functions for params in calls]

    # Return lower bound of call count for functions colored with yellow
    def yellow_count(self):
        return round(self._model.yellow_count())

    # Return lower bound of call count for functions colored with red
    def red_count(self):
        return round(self._model.red_count())

    # Return the maximum of call counts for all functions
    def max_count(self):
        return self._model.max_count()

    # Event for static output submit button clicked
    def output_submit_btn_clicked(self, text):
        self._model = StaticModel()
        self._model.load_text(text)

    # Event for starting trace with functions given in dictionary
    def trace_with_ui_elements(self, trace_dict):
        self._model = DynamicModel()
        self._model.trace_dict(trace_dict)

    # Event for starting trace with functions given in config file
    def trace_with_config_file(self, config_path):
        self._model = DynamicModel()
        self._model.trace_yaml(config_path)

    # Event for tracing stopped
    def trace_btn_turned_off(self):
        self._model.stop_trace()

    # Event for setting colors
    def set_range(self, range_bottom, range_top):
        self._model.set_range(range_bottom, range_top)

    # Return error happening while tracing
    def thread_error(self):
        return self._model.thread_error()

    # Return error happening while processing functions to trace
    def process_error(self):
        return self._model.process_error()

    # Return status of tracing
    def trace_active(self):
        return self._model.trace_active()
