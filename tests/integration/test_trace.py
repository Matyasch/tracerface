from contextlib import contextmanager
from pathlib import Path
import subprocess
import time

from pytest import fixture

from tracerface.call_graph import CallGraph
from tracerface.trace_controller import TraceController
from tracerface.web_ui.trace_setup import Setup
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


@contextmanager
def create_test_binary(dest_dir):
    source_path = Path(__file__).parent.parent.joinpath('resources', 'test_application.c')
    dest_path = dest_dir.joinpath('test_application')
    compile_command = ['gcc', '-ggdb3', '-O0', '-fno-omit-frame-pointer', '-o']
    compile_command += [str(dest_path), str(source_path)]
    try:
        subprocess.run(compile_command)
        yield str(dest_path)
    finally:
        dest_path.unlink()


def test_trace(tmp_path):
    call_graph = CallGraph()
    setup = Setup()
    trace_controller = TraceController()

    with create_test_binary(tmp_path) as app:
        setup.initialize_binary(app)
        setup.setup_function_to_trace(app, 'func1')
        setup.setup_function_to_trace(app, 'func2')
        setup.setup_function_to_trace(app, 'func3')
        setup.add_parameter(app, 'func1', '1', '%s')
        setup.add_parameter(app, 'func1', '2', '%s')
        setup.add_parameter(app, 'func2', '1', '%d')

        trace_controller.start_trace(setup.generate_bcc_args(), call_graph) # start monitoring
        time.sleep(5) # BCC trace needs a bit of time to setup
        subprocess.run(app) # run monitored application
        trace_controller.stop_trace() # stop

    edges = convert_edges_to_cytoscape_format(call_graph.get_nodes(), call_graph.get_edges())
    nodes = convert_nodes_to_cytoscape_format(call_graph.get_nodes(), call_graph.get_edges())
    assert_results(nodes, edges)
