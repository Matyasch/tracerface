'''
This module contains the definitions of all the styles used by elements
'''

def tab_style():
    return {'padding': '0px 20px 0px 20px'}


def button_style():
    return {'margin-top': '10px'}


def element_style():
    return {'margin-top': '10px'}


def base_node_style():
    return {
        'selector': 'node',
        'style': {
            'content': 'data(name)',
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
    }


def green_node_style(yellow_count, search):
    return {
        'selector': '[count > 0][count < {}][name *= "{}"]'.format(yellow_count, search),
        'style': {
            'border-color': 'green',
            'color': 'green'
        }
    }


def yellow_node_style(yellow_count, red_count, search):
    return {
        'selector': '[count >= {}][count < {}][name *= "{}"]'.format(yellow_count,
                                                                     red_count, search),
        'style': {
            'border-color': 'orange',
            'color': 'orange'
        }
    }


def red_node_style(red_count, search):
    return {
        'selector': '[count >= {}][name *= "{}"]'.format(red_count, search),
        'style': {
            'border-color': 'red',
            'color': 'red'
        }
    }


def base_edge_style():
    return {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#ccc',
            'label': 'data(params)',
            'line-color': '#ccc'
        }
    }


def green_edge_style(yellow_count, search):
    return {
        'selector': '[call_count > 0][call_count < {}][called_name *= "{}"]'.format(yellow_count, search),
        'style': {
            'line-color': 'green',
            'target-arrow-color': 'green',
            'width': '1'
        }
    }


def yellow_edge_style(yellow_count, red_count, search):
    return {
        'selector': '[call_count >= {}][call_count < {}][called_name *= "{}"]'.format(yellow_count, red_count, search),
        'style': {
            'line-color': 'orange',
            'target-arrow-color': 'orange',
            'width': '1'
        }
    }


def red_edge_style(red_count, search):
    return {
        'selector': '[call_count >= {}][called_name *= "{}"]'.format(red_count, search),
        'style': {
            'line-color': 'red',
            'target-arrow-color': 'red',
            'width': '1'
        }
    }
