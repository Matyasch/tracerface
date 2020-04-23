'''
This module contains the definitions of all the styles used by elements
'''


def element_style():
    return {'margin-top': '10px'}


def expanded_style(node_id):
    return {
        'selector': '#{}'.format(node_id),
        'style': {
            'label': 'data(info)',
            'text-wrap': 'wrap'
        }
    }


def node_styles(yellow_count, red_count, search):
    return [
        {
            'selector': 'node',
            'style': {
                'label': 'data(name)',
                'text-valign': 'center',
                'width': 'label',
                'height': 'label',
                'shape': 'rectangle',
                'border-color': 'grey',
                'color': 'grey',
                'background-color': 'white',
                'border-width': '1',
                'padding': '5px'
            }
        },
        {
            'selector': '[count > 0][count < {}][name *= "{}"]'.format(yellow_count, search),
            'style': {
                'border-color': 'green',
                'color': 'green'
            }
        },
        {
            'selector': '[count >= {}][count < {}][name *= "{}"]'.format(yellow_count,
                                                                        red_count, search),
            'style': {
                'border-color': 'orange',
                'color': 'orange'
            }
        },
        {
            'selector': '[count >= {}][name *= "{}"]'.format(red_count, search),
            'style': {
                'border-color': 'red',
                'color': 'red'
            }
        },
    ]


def edge_styles(yellow_count, red_count, search):
    return [
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'target-arrow-color': '#ccc',
                'label': 'data(params)',
                'line-color': '#ccc'
            }
        },
        {
            'selector': '[call_count > 0][call_count < {}][called_name *= "{}"]'.format(yellow_count, search),
            'style': {
                'line-color': 'green',
                'target-arrow-color': 'green',
                'width': '1'
            }
        },
        {
            'selector': '[call_count >= {}][call_count < {}][called_name *= "{}"]'.format(yellow_count, red_count, search),
            'style': {
                'line-color': 'orange',
                'target-arrow-color': 'orange',
                'width': '1'
            }
        },
        {
            'selector': '[call_count >= {}][called_name *= "{}"]'.format(red_count, search),
            'style': {
                'line-color': 'red',
                'target-arrow-color': 'red',
                'width': '1'
            }
        }
    ]
