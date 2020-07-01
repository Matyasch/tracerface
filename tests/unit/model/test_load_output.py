#!/usr/bin/env python3
from pathlib import Path
from unittest import main, TestCase

from model.load_output import load_trace_output_from_file_to_call_graph
from persistence.call_graph import CallGraph
from tests.integration.test_trace import EXPECTED_NODES


class TestLoadFromFile(TestCase):
    def test_load_output_happy_case(self):
        test_file_path = Path(__file__).absolute().parent.parent.parent.joinpath(
            'integration', 'resources', 'test_static_output'
        )
        call_graph = CallGraph()
        load_trace_output_from_file_to_call_graph(str(test_file_path), call_graph)
        result_nodes = call_graph.get_nodes().values()
        sorted_nodes = sorted(result_nodes, key = lambda node: node['name'])
        for result, expected in zip(sorted_nodes, EXPECTED_NODES):
            assert result['name'] == expected['name']
            assert result['call_count'] == expected['count']
            assert result['source'] == expected['source']


if __name__ == '__main__':
    main()
