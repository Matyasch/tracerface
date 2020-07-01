#!/usr/bin/env python3
# Transforms data into format usable by the layout
class ViewModel:
    def __init__(self, call_graph, setup, trace_controller):
        self._call_graph = call_graph
        self._setup = setup
        self._trace_controller = trace_controller
        self._expanded_elements = []

    # Return list of nodes in a format usable to the view
    def get_nodes(self):
        return [
            {
                'data': {
                    'id': node_id,
                    'name': self._call_graph.get_nodes()[node_id]['name'],
                    'info': self.get_info_text_for_node(node_id),
                    'source': self._call_graph.get_nodes()[node_id]['source'],
                    'count': self._call_graph.get_nodes()[node_id]['call_count']
                }
            } for node_id in self._call_graph.get_nodes()
        ]

    # Return list of edges in a format usable to the view
    def get_edges(self):
        return [
            {
                'data': {
                    'source': edge[0],
                    'target': edge[1],
                    'params': self.get_param_visuals_for_edge(edge),
                    'call_count': self._call_graph.get_edges()[edge]['call_count'],
                    'caller_name': self._call_graph.get_nodes()[edge[0]]['name'],
                    'called_name': self._call_graph.get_nodes()[edge[1]]['name'],
                    'info': self.get_info_text_for_edge(edge)
                }
            } for edge in self._call_graph.get_edges()
        ]

    def get_info_text_for_node(self, id):
        node = self._call_graph.get_nodes()[id]
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
        edge = self._call_graph.get_edges()[id]
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
        calls = self._call_graph.get_edges()[edge]['params']
        if len(calls) == 0:
            return ''
        elif len(calls) == 1:
            return ', '.join(calls[0])
        return '...'

    # Return parameters for an edge defined by its source and target
    def get_params_of_edge(self, source, target):
        return self._call_graph.get_edges()[(source, target)]['params']

    # Return parameters for a node defined by its id/hash
    def get_params_of_node(self, node_id):
        params_by_functions = [self._call_graph.get_edges()[edge]['params'] for edge in self._call_graph.get_edges() if str(edge[1]) == node_id]
        return [params for calls in params_by_functions for params in calls]

    def element_clicked(self, id):
        if id in self._expanded_elements:
            self._expanded_elements.remove(id)
        else:
            self._expanded_elements.append(id)

    def get_expanded_elements(self):
        return self._expanded_elements
