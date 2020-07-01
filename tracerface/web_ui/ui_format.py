#!/usr/bin/env python3
'''
This module contains functions to convert
data in the call graph into the format
which dash cytoscape requires
'''

# Returns list of nodes in a format usable to cytoscape
def convert_nodes_to_cytoscape_format(nodes, edges):
    return [
        {
            'data': {
                'id': node_id,
                'name': nodes[node_id]['name'],
                'source': nodes[node_id]['source'],
                'count': nodes[node_id]['call_count'],
                'info': _get_info_text_for_node(nodes[node_id], _get_params_of_node(node_id, edges))
            }
        } for node_id in nodes
    ]

# Returns list of edges in a format usable to cytoscape
def convert_edges_to_cytoscape_format(nodes, edges):
    return [
        {
            'data': {
                'source': edge[0],
                'target': edge[1],
                'params': _get_param_visuals_for_edge(edges[edge]['params']),
                'call_count': edges[edge]['call_count'],
                'caller_name': nodes[edge[0]]['name'],
                'called_name': nodes[edge[1]]['name'],
                'info': _get_info_text_for_edge(edges[edge])
            }
        } for edge in edges
    ]

# Returns text containing information about given node
def _get_info_text_for_node(node, params):
    text = '{}\nSource: {}\nCalled {} times'.format(
        node['name'],
        node['source'],
        node['call_count']
    )
    if len(params) > 0:
        text = '{}\nWith parameters:\n{}'.format(
            text,
            '\n'.join([', '.join(param) for param in params])
        )
    return text

# Returns text containing information about given edge
def _get_info_text_for_edge(edge):
    text = 'Call made {} times'.format(edge['call_count'])
    params = edge['params']
    if len(params) > 0:
        text = '{}\nWith parameters:\n{}'.format(
            text,
            '\n'.join([', '.join(param) for param in params])
        )
    return text

# Returns label of a given edge based on its parameters
def _get_param_visuals_for_edge(params):
    if len(params) == 0:
        return ''
    elif len(params) == 1:
        return ', '.join(params[0])
    else:
        return '...'

# Returns parameters for a node defined by its id/hash
def _get_params_of_node(node_id, edges):
    params_by_calls = [edges[edge]['params'] for edge in edges if str(edge[1]) == node_id]
    return [params for calls in params_by_calls for params in calls]
