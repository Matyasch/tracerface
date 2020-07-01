from pytest import fixture
import unittest.mock as mock

from model.trace_controller import TraceController
from persistence.call_graph import CallGraph
from viewmodel.trace_setup import Setup
from viewmodel.viewmodel import ViewModel


@fixture
def nodes():
    return {
        'dummy_hash1': {
            'name': 'dummy_name1',
            'source': 'dummy_source1',
            'call_count': 0
        },
        'dummy_hash2': {
            'name': 'dummy_name2',
            'source': 'dummy_source2',
            'call_count': 1
        },
        'dummy_hash3': {
            'name': 'dummy_name3',
            'source': 'dummy_source1',
            'call_count': 2
        }
    }


@fixture
def edges():
    return {
        ('dummy_hash1', 'dummy_hash2'): {
            'params': [],
            'call_count': 0
        },
        ('dummy_hash1', 'dummy_hash3'): {
            'params': [['dummy_param']],
            'call_count': 3
        },
        ('dummy_hash2', 'dummy_hash3'): {
            'params': [['dummy_param1'], ['dummy_param2'], ['dummy_param3']],
            'call_count': 4
        }
    }


def test_get_param_visuals(edges):
    call_graph = mock.Mock()
    call_graph.get_edges.return_value = edges
    viewmodel = ViewModel(call_graph, Setup(), TraceController(call_graph))

    assert viewmodel.get_param_visuals_for_edge(('dummy_hash1', 'dummy_hash2')) == ''
    assert viewmodel.get_param_visuals_for_edge(('dummy_hash1', 'dummy_hash3')) == 'dummy_param'
    assert viewmodel.get_param_visuals_for_edge(('dummy_hash2', 'dummy_hash3')) == '...'


def test_get_params_of_edge(edges):
    call_graph = mock.Mock()
    call_graph.get_edges.return_value = edges
    viewmodel = ViewModel(call_graph, Setup(), TraceController(call_graph))

    assert viewmodel.get_params_of_edge('dummy_hash1', 'dummy_hash2') == []
    assert viewmodel.get_params_of_edge('dummy_hash1', 'dummy_hash3') == [['dummy_param']]
    assert viewmodel.get_params_of_edge('dummy_hash2', 'dummy_hash3') == [
        ['dummy_param1'], ['dummy_param2'], ['dummy_param3']
    ]


def test_get_params_of_node(edges, nodes):
    call_graph = mock.Mock()
    call_graph.get_edges.return_value = edges
    call_graph.get_nodes.return_value = nodes
    viewmodel = ViewModel(call_graph, Setup(), TraceController(call_graph))

    assert viewmodel.get_params_of_node('dummy_hash2') == []
    assert viewmodel.get_params_of_node('dummy_hash3') == [
        ['dummy_param'], ['dummy_param1'], ['dummy_param2'], ['dummy_param3']
    ]
