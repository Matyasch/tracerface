from pathlib import Path
import subprocess
import time

from pytest import fixture

from tracerface.trace_controller import TraceController
from tracerface.call_graph import CallGraph
from tracerface.trace_setup import Setup
from tracerface.web_ui.ui_format import (
    convert_edges_to_cytoscape_format,
    convert_nodes_to_cytoscape_format
)


EXPECTED_NODES = [
    {'name': '__libc_start_main', 'count': 0, 'source': 'libc-2.27.so'},
    {'name': 'func1', 'count': 2, 'source': 'test_application'},
    {'name': 'func2', 'count': 1, 'source': 'test_application'},
    {'name': 'func3', 'count': 5, 'source': 'test_application'},
    {'name': 'func6', 'count': 0, 'source': 'test_application'},
    {'name': 'main', 'count': 0, 'source': 'test_application'}
]


EXPECTED_EDGES = [
    {'call_count': 2, 'called_name': 'func1', 'caller_name': 'func6', 'params': '...'},
    {'call_count': 1, 'called_name': 'func2', 'caller_name': 'func6', 'params': '3'},
    {'call_count': 5, 'called_name': 'func3', 'caller_name': 'func6', 'params': ''},
    {'call_count': 0, 'called_name': 'func6', 'caller_name': 'main', 'params': ''},
    {'call_count': 0, 'called_name': 'main', 'caller_name': '__libc_start_main', 'params': ''}
]


def assert_results(result_nodes, result_edges):
    assert len(result_nodes) == len(EXPECTED_NODES)
    assert len(result_edges) == len(EXPECTED_EDGES)

    sorted_nodes = sorted(result_nodes, key = lambda i: i['data']['name'])
    # we can sort like this because no node is called from two different nodes
    sorted_edges = sorted(result_edges, key = lambda i: i['data']['called_name'])

    for result, expected in zip(sorted_nodes, EXPECTED_NODES):
        assert result['data']['name'] == expected['name']
        assert result['data']['count'] == expected['count']
        assert result['data']['source'] == expected['source']
    for result, expected in zip(sorted_edges, EXPECTED_EDGES):
        assert result['data']['call_count'] == expected['call_count']
        assert result['data']['called_name'] == expected['called_name']
        assert result['data']['caller_name'] == expected['caller_name']
        assert result['data']['params'] == expected['params']


@fixture
def test_binary(tmp_path):
    source_path = Path(__file__).parent.parent.joinpath('resources', 'test_application.c')
    dest_path = tmp_path.joinpath('test_application')
    compile_command = ['gcc', '-ggdb3', '-O0', '-fno-omit-frame-pointer', '-o']
    compile_command += [str(dest_path), str(source_path)]
    subprocess.run(compile_command)
    return str(dest_path)


def test_trace(test_binary):
    call_graph = CallGraph()
    setup = Setup()
    trace_controller = TraceController(call_graph)

    setup.initialize_binary(test_binary)
    setup.setup_function_to_trace(test_binary, 'func1')
    setup.setup_function_to_trace(test_binary, 'func2')
    setup.setup_function_to_trace(test_binary, 'func3')
    setup.add_parameter(test_binary, 'func1', '1', '%s')
    setup.add_parameter(test_binary, 'func1', '2', '%s')
    setup.add_parameter(test_binary, 'func2', '1', '%d')

    trace_controller.start_trace(setup.generate_bcc_args()) # start monitoring
    time.sleep(5) # BCC trace needs a bit of time to setup
    subprocess.run(test_binary) # run monitored application
    trace_controller.stop_trace() # stop

    edges = convert_edges_to_cytoscape_format(call_graph.get_nodes(), call_graph.get_edges())
    nodes = convert_nodes_to_cytoscape_format(call_graph.get_nodes(), call_graph.get_edges())
    assert_results(nodes, edges)
