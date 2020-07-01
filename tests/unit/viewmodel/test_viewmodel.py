from pathlib import Path
from pytest import fixture, raises
import unittest.mock as mock

from model.parse_stack import Stack
from model.trace_controller import TraceController
from persistence.call_graph import CallGraph
from viewmodel.trace_setup import Setup
from viewmodel.viewmodel import ViewModel

from tests.integration.test_trace import EXPECTED_NODES


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


@mock.patch('viewmodel.viewmodel.Path.read_text')
def test_load_output_from_directory(read):
    read.side_effect = IsADirectoryError
    call_graph = CallGraph()
    viewmodel = ViewModel(call_graph, Setup(), TraceController(call_graph))

    with raises(ValueError):
        viewmodel.load_output('/direcory/path')


@mock.patch('viewmodel.viewmodel.Path.read_text')
def test_load_output_from_directory(read):
    read.side_effect = FileNotFoundError
    call_graph = CallGraph()
    viewmodel = ViewModel(call_graph, Setup(), TraceController(call_graph))

    with raises(ValueError):
        viewmodel.load_output('.non/existent/path')


def test_load_output_happy_case():
    test_file_path = Path(__file__).absolute().parent.parent.parent.joinpath(
        'integration', 'resources', 'test_static_output'
    )
    call_graph = CallGraph()
    viewmodel = ViewModel(call_graph, Setup(), TraceController(call_graph))
    viewmodel.load_output(str(test_file_path))
    result_nodes = viewmodel.get_nodes()
    sorted_nodes = sorted(result_nodes, key = lambda i: i['data']['name'])
    for result, expected in zip(sorted_nodes, EXPECTED_NODES):
        assert result['data']['name'] == expected['name']
        assert result['data']['count'] == expected['count']
        assert result['data']['source'] == expected['source']


def test_expanded_elements():
    call_graph = CallGraph()
    viewmodel = ViewModel(call_graph, Setup(), TraceController(call_graph))
    viewmodel.element_clicked('dummy_id1')
    assert 'dummy_id1' in viewmodel._expanded_elements

    viewmodel.element_clicked('dummy_id2')
    assert 'dummy_id1' in viewmodel._expanded_elements
    assert 'dummy_id2' in viewmodel._expanded_elements

    viewmodel.element_clicked('dummy_id1')
    assert 'dummy_id1' not in viewmodel._expanded_elements
