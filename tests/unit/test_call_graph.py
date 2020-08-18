#!/usr/bin/env python3
from unittest import main, TestCase

from tracerface.call_graph import CallGraph


class TestConstructor(TestCase):
    def test_initial_call_graph(self):
        call_graph = CallGraph()
        self.assertEqual(call_graph._nodes, {})
        self.assertEqual(call_graph._edges, {})
        self.assertEqual(call_graph._yellow, 0)
        self.assertEqual(call_graph._red, 0)


class TestGetNodes(TestCase):
    def test_get_nodes_returns_empty_dict_for_empty_call_graph(self):
        call_graph = CallGraph()
        self.assertEqual(call_graph.get_nodes(), {})

    def test_get_nodes_returns_loaded_nodes(self):
        call_graph = CallGraph()
        call_graph.load_nodes({
            'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
        })
        expected_nodes = {
            'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
        }
        self.assertEqual(call_graph.get_nodes(), expected_nodes)


class TestGetEdges(TestCase):
    def test_get_edges_returns_empty_dict_for_empty_call_graph(self):
        call_graph = CallGraph()
        self.assertEqual(call_graph.get_edges(), {})

    def test_get_edges_returns_loaded_edges(self):
        call_graph = CallGraph()
        call_graph.load_edges({
            ('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0},
            ('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}
        })
        expected_edges = {
            ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
            ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
        }
        self.assertEqual(call_graph.get_edges(), expected_edges)


class TestLoadNodes(TestCase):
    def test_load_nodes_updates_returned_nodes(self):
        call_graph = CallGraph()
        call_graph.load_nodes({
            'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
        })
        call_graph.load_nodes({
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source1', 'call_count': 5},
            'dummy_hash3': {'name': 'dummy_name3', 'source': 'dummy_source2', 'call_count': 2}
        })
        expected_nodes = {
            'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 6},
            'dummy_hash3': {'name': 'dummy_name3', 'source': 'dummy_source2', 'call_count': 2}
        }
        self.assertEqual(call_graph.get_nodes(), expected_nodes)


class TestLoadEdges(TestCase):
    def test_load_edges_updates_returned_edges(self):
        call_graph = CallGraph()
        call_graph.load_edges({
            ('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0},
            ('node_hash3', 'node_hash4'): {'param': ['dummy_param1'], 'call_count': 3}
        })
        call_graph.load_edges({
            ('node_hash2', 'node_hash3'): {'param': [], 'call_count': 2},
            ('node_hash3', 'node_hash4'): {'param': ['dummy_param2', 'dummy_param3'], 'call_count': 3}
        })
        expected_edges = {
            ('node_hash1', 'node_hash2'): {
                'params': [], 'call_count': 0
            },
            ('node_hash2', 'node_hash3'): {
                'params': [], 'call_count': 2
            },
            ('node_hash3', 'node_hash4'): {
                'params': [['dummy_param1'], ['dummy_param2', 'dummy_param3']], 'call_count': 6
            }
        }
        self.assertEqual(call_graph.get_edges(), expected_edges)


class TestClear(TestCase):
    def test_clear_removes_all_nodes_and_edges_and_color_boundaries(self):
        call_graph = CallGraph()
        call_graph.load_nodes({
            'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
        })
        call_graph.load_edges({
            ('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0},
            ('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}
        })
        call_graph.clear()
        self.assertEqual(call_graph.get_nodes(), {})
        self.assertEqual(call_graph.get_edges(), {})
        self.assertEqual(call_graph.get_yellow(), 0)
        self.assertEqual(call_graph.get_red(), 0)


class TestSetColors(TestCase):
    def test_set_colors_sets_returned_colors(self):
        call_graph = CallGraph()
        call_graph.set_colors(yellow=2, red=3)
        self.assertEqual(call_graph.get_yellow(), 2)
        self.assertEqual(call_graph.get_red(), 3)


    def test_set_colors_updates_existing_colors(self):
        call_graph = CallGraph()
        call_graph.set_colors(yellow=2, red=3)
        call_graph.set_colors(yellow=5, red=6)
        self.assertEqual(call_graph.get_yellow(), 5)
        self.assertEqual(call_graph.get_red(), 6)


class TestInitColors(TestCase):
    def test_init_colors_sets_colors_based_on_node_call_counts(self):
        call_graph = CallGraph()
        call_graph.load_nodes({
            'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 10},
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
        })
        call_graph.init_colors()
        self.assertEqual(call_graph.get_yellow(), 3)
        self.assertEqual(call_graph.get_red(), 6)


class TestMaxCount(TestCase):
    def test_max_count_returns_maximum_call_count_among_nodes(self):
        call_graph = CallGraph()
        call_graph.load_nodes({
            'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 10},
            'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
        })
        self.assertEqual(call_graph.max_count(), 10)


class TestExpandElements(TestCase):
    def test_element_clicked_adds_element_to_returned_elements(self):
        call_graph = CallGraph()
        call_graph.element_clicked('dummy_id')
        self.assertEqual(call_graph.get_expanded_elements(), ['dummy_id'])

    def test_element_clicked_removes_element_to_returned_elements(self):
        call_graph = CallGraph()
        call_graph.element_clicked('dummy_id1')
        call_graph.element_clicked('dummy_id2')
        call_graph.element_clicked('dummy_id1')
        self.assertEqual(call_graph.get_expanded_elements(), ['dummy_id2'])


if __name__ == '__main__':
    main()
