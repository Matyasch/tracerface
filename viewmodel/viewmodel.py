from pathlib import Path

from model.model import Model
from persistence.persistence import Persistence


# Transforms data into format usable by the layout
class ViewModel:
    def __init__(self, setup):
        self._model = Model(Persistence())
        self._setup = setup
        self._expanded_elements = []

    # Return list of nodes in a format usable to the view
    def get_nodes(self):
        return [
            {
                'data': {
                    'id': node_id,
                    'name': self._model.get_nodes()[node_id]['name'],
                    'info': self.get_info_text_for_node(node_id),
                    'source': self._model.get_nodes()[node_id]['source'],
                    'count': self._model.get_nodes()[node_id]['call_count']
                }
            } for node_id in self._model.get_nodes()
        ]

    # Return list of edges in a format usable to the view
    def get_edges(self):
        return [
            {
                'data': {
                    'source': edge[0],
                    'target': edge[1],
                    'params': self.get_param_visuals_for_edge(edge),
                    'call_count': self._model.get_edges()[edge]['call_count'],
                    'caller_name': self._model.get_nodes()[edge[0]]['name'],
                    'called_name': self._model.get_nodes()[edge[1]]['name'],
                    'info': self.get_info_text_for_edge(edge)
                }
            } for edge in self._model.get_edges()
        ]

    def get_info_text_for_node(self, id):
        node = self._model.get_nodes()[id]
        text = '{}\nSource: {}\nCalled {} times'.format(
            node['name'],
            node['source'],
            node['call_count'])
        params = self.get_params_of_node(id)
        if len(params) > 0:
            text = '{}\nWith parameters:\n{}'.format(
                text,
                '\n'.join([', '.join(param) for param in params])
            )
        return text

    def get_info_text_for_edge(self, id):
        edge = self._model.get_edges()[id]
        text = 'Call made {} times'.format(edge['call_count'])
        params = self.get_params_of_edge(id[0], id[1])
        if len(params) > 0:
            text = '{}\nWith parameters:\n{}'.format(
                text,
                '\n'.join([', '.join(param) for param in params])
            )
        return text

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
    def load_output(self, path):
        if not path:
            return
        try:
            text = Path(path).read_text()
        except FileNotFoundError:
            raise ValueError('Could not find output file at {}'.format(path))
        except IsADirectoryError:
            raise ValueError('{} is a directory, not a file'.format(path))
        self._model = Model(Persistence())
        self._model.load_output(text)

    # Create arguments from setup and start tracing
    def start_trace(self):
        self._model = Model(Persistence())
        arguments = self._setup.generate_bcc_args()
        self._model.start_trace(arguments)

    # Stop trace
    def stop_trace(self):
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

    # Returns a dict of pairs of functions name and False
    def add_app(self, app):
        try:
            self._setup.initialize_binary(app)
            return ''
        except ValueError as err:
            self._setup.initialize_built_in(app)
            return str(err)

    # Remove application from getting traced
    def remove_app(self, app):
        if app:
            self._setup.remove_app(app)

    # Returns apps currently saved in model
    def get_apps(self):
        return self._setup.get_apps()

    # Returns functions which are set to be traced
    def get_traced_functions_for_app(self, app):
        if not app:
            return []
        app_setup = self._setup.get_setup_of_app(app)
        return [func for func in app_setup if app_setup[func]['traced']]

    # Returns functions which are not set to be traced
    def get_not_traced_functions_for_app(self, app):
        if not app:
            return []
        app_setup = self._setup.get_setup_of_app(app)
        return [func for func in app_setup if not app_setup[func]['traced']]

    # Sets up a function to be traced
    def add_function(self, app, function):
        if app and function:
            self._setup.setup_function_to_trace(app, function)

    # Removes a function from traced ones
    def remove_function(self, app, function):
        if app and function:
            self._setup.remove_function_from_trace(app, function)

    # Returns the indexes where a parameter is set for tracing
    def get_parameters(self, app, function):
        if app and function:
            return self._setup.get_parameters(app, function)
        return {}

    # Sets up a parameter to be traced
    def add_parameter(self, app, function, index, format):
        if app and function and index and format:
            self._setup.add_parameter(app, function, index, format)

    # Removes a parameter from traced ones
    def remove_parameter(self, app, function, index):
        if app and function and index:
            self._setup.remove_parameter(app, function, int(index))

    def load_config_file(self, path):
        if path:
            return self._setup.load_from_file(path)

    def element_clicked(self, id):
        if id in self._expanded_elements:
            self._expanded_elements.remove(id)
        else:
            self._expanded_elements.append(id)

    def get_expanded_elements(self):
        return self._expanded_elements
