#!/usr/bin/env python3
from unittest import main, TestCase

from tracerface.web_ui.ui_format import (
    convert_edges_to_cytoscape_format,
    convert_nodes_to_cytoscape_format
)


class TestConvertNodes(TestCase):
    def _edges(self):
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

    def test_convert_node_without_params(self):
        nodes = {
            'dummy_hash1': {
                'name': 'dummy_name1',
                'source': 'dummy_source1',
                'call_count': 0
            }
        }
        expected = [{
            'data': {
                'id': 'dummy_hash1',
                'name': 'dummy_name1',
                'source': 'dummy_source1',
                'count': 0,
                'info': 'dummy_name1\nSource: dummy_source1\nCalled 0 times'
            }
        }]
        result = convert_nodes_to_cytoscape_format(nodes, self._edges())
        self.assertEqual(result, expected)

    def test_convert_node_with_params(self):
        nodes = {
            'dummy_hash3': {
                'name': 'dummy_name3',
                'source': 'dummy_source1',
                'call_count': 2
            }
        }
        expected_info = 'dummy_name3\n' + 'Source: dummy_source1\n' + 'Called 2 times\n'
        expected_info += 'With parameters:\n' + 'dummy_param\n' + 'dummy_param1\n'
        expected_info += 'dummy_param2\n' + 'dummy_param3'
        expected = [{
            'data': {
                'id': 'dummy_hash3',
                'name': 'dummy_name3',
                'source': 'dummy_source1',
                'count': 2,
                'info': expected_info,
            }
        }]
        result = convert_nodes_to_cytoscape_format(nodes, self._edges())
        self.assertEqual(result, expected)



class TestConvertEdges(TestCase):
    def _nodes(self):
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
    def test_convert_edge_without_params(self):
        edges = {
            ('dummy_hash1', 'dummy_hash2'): {
                'params': [],
                'call_count': 0
            }
        }
        expected = [{
            'data': {
                    'call_count': 0,
                    'called_name': 'dummy_name2',
                    'caller_name': 'dummy_name1',
                    'info': 'Call made 0 times',
                    'params': '',
                    'source': 'dummy_hash1',
                    'target': 'dummy_hash2'
            }
        }]
        result = convert_edges_to_cytoscape_format(self._nodes(), edges)
        self.assertEqual(result, expected)

    def test_convert_edge_with_single_param(self):
        edges = {
            ('dummy_hash1', 'dummy_hash3'): {
                'params': [['dummy_param']],
                'call_count': 3
            }
        }
        expected = [{
            'data': {
                'call_count': 3,
                'called_name': 'dummy_name3',
                'caller_name': 'dummy_name1',
                'info': 'Call made 3 times\nWith parameters:\ndummy_param',
                'params': 'dummy_param',
                'source': 'dummy_hash1',
                'target': 'dummy_hash3'
            }
        }]
        result = convert_edges_to_cytoscape_format(self._nodes(), edges)
        self.assertEqual(result, expected)

    def test_convert_edge_with_multiple_params(self):
        edges = {
            ('dummy_hash2', 'dummy_hash3'): {
                'params': [['dummy_param1'], ['dummy_param2'], ['dummy_param3']],
                'call_count': 4
            }
        }
        expected_info = 'Call made 4 times\n' + 'With parameters:\n'
        expected_info += 'dummy_param1\n' + 'dummy_param2\n' + 'dummy_param3'
        expected = [{
            'data': {
                'call_count': 4,
                'called_name': 'dummy_name3',
                'caller_name': 'dummy_name2',
                'info': expected_info,
                'params': '...',
                'source': 'dummy_hash2',
                'target': 'dummy_hash3'
            }
        }]
        result = convert_edges_to_cytoscape_format(self._nodes(), edges)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    main()
